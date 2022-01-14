#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 9
#define AOC_YEAR 2021

#ifdef TEST
#define BITSTREAM_LENGTH 25
#else
#define BITSTREAM_LENGTH 4096
#endif

struct bitvector {
    unsigned char bitstream[BITSTREAM_LENGTH];
    int length;
};

unsigned long getbits(struct bitvector * b, int position, int nbits)
{
    unsigned long retval = 0;
    int firstchar, lastchar, firstbit, lastbit;
    unsigned char mask = 0;
    int charindex, bitindex;

    firstchar = position / 8;
    firstbit = position % 8;
    lastchar = (position + nbits) / 8;
    lastbit = (position + nbits) % 8;

    //DBGPRINT("-- getting %u bits at %u: %u.%u - %u.%u\n",
    //        nbits, position, firstchar, firstbit, lastchar, lastbit);
    if(nbits > sizeof(retval) * 8)
    {
        printf("ERROR: asked to retrieve %d bits, which don't fit in"
               " an unsigned long\n", nbits);
        exit(1);
    }

    if(position + nbits > b->length)
    {
        printf("ERROR: requested %d bits at %d, but bitvector has only %d\n",
                nbits, position, b->length);
        exit(1);
    }

    if(firstchar == lastchar)
    {
        for(bitindex=firstbit; bitindex < lastbit; bitindex++)
        {
            mask |= 1 << (7-bitindex);
        }
        retval = (b->bitstream[firstchar] & mask) >> (8 - lastbit);
    }
    else
    {
        /* first char */
        for(bitindex=firstbit; bitindex < 8; bitindex++)
            mask |= 1<<(7-bitindex);
        retval |= b->bitstream[firstchar] & mask;
        
//printf("### %d bits from [%d]%02x gives %d\n", firstbit, firstchar,b->bitstream[firstchar], retval);
        /* full chars */
        for(charindex = firstchar + 1; charindex < lastchar;
                charindex++)
        {
            retval = (retval << 8) | b->bitstream[charindex];
//printf("#### %d bits from [%d]%02x gives %d\n", 8, charindex, b->bitstream[charindex], retval);
        }

        /* remaining bits */
        retval = (retval << lastbit) |
            (b->bitstream[lastchar] >> (8 - lastbit));
//printf("### %d bits from [%d]%02x gives %d\n", 8 - lastbit, lastchar, b->bitstream[lastchar], retval);
    }
//printf("### returning %d\n", retval);
printf("### %d bits at %d (%d.%d) gives %d: ", nbits, position, firstchar, firstbit, retval);
for(int q=firstchar; q <=lastchar; q++)
{
    printf("%02x", b->bitstream[q]);
}
printf("\n");
    return retval;
}

int test()
{
#define TEST_BITVECTOR_SIZE 2
    /* 0x35AC is 0011 0101 1010 1100 */
    struct testcase_t {
        int position;
        int nbits;
        unsigned long expected_answer;
    };
    struct testcase_t testcases[] = {
        { 0, 1, 0 },
        { 0, 3, 1 },
        { 0, 4, 3 },
        { 1, 3, 3 },
        { 3, 1, 1 },

        { 4, 1, 0 },
        { 4, 3, 2 },
        { 4, 4, 5 },
        { 5, 3, 5 },
        { 7, 1, 1 },

        { 0, 5, 6 },
        { 0, 7, 0x35 >> 1 },
        { 0, 8, 0x35 },
        { 1, 4, 3 << 1 },
        { 1, 5, 3 << 2 | 1 },
        { 1, 7, 0x35 },
        { 1, 8, 0x35 << 1 | 1 },
        { 3, 4, (1 << 3) | (0x5 >> 1) },
        { 3, 5, (1 << 4) | 0x5 },
        { 3, 8, (1 << 7) | (0x5A >> 1) },
        { 3, 9, (1 << 8) | 0x5A },
        { 3, 10, (1 << 9) | (0x5A << 1) | 1 },
        { 4, 8, 0x5A },
        { 4, 9, (0x5A << 1) | 1 },
    };
    struct bitvector b;
    int nerrs = 0;
    struct testcase_t * testcase;
    int testcasen;
    unsigned long answer;

    b.bitstream[0] = 0x35;
    b.bitstream[1] = 0xAC;
    b.length = 16;

    for(testcasen = 0;
        testcasen < sizeof(testcases)/sizeof(testcases[0]);
        testcasen++)
    {
        testcase = &testcases[testcasen];
        b.length = TEST_BITVECTOR_SIZE * 8;
        answer = getbits(&b,
                testcase->position, testcase->nbits);
        if(answer != testcase->expected_answer)
        {
            printf("ERROR: testcase %d, %d bits at position %d,"
                    " expected %08lx, received %08lx\n", testcasen,
                    testcase->nbits, testcase->position,
                    testcase->expected_answer, answer);
            nerrs++;
        }
    }

    if(nerrs > 0)
    {
        printf("testing FAILED! %u/%lu errors\n", nerrs,
            sizeof(testcases)/sizeof(testcases[0]));
    }
    else
    {
        printf("testing SUCCEEDED! passed %lu tests\n",
            sizeof(testcases)/sizeof(testcases[0]));
    }

    return nerrs;
}

int parse_header(
        int * version,
        int * typeid,
        int * end,
        int * version_sum,
        struct bitvector * b,
        int start)
{
    /* get the version */
    *version = getbits(b, start, 3);
    *typeid = getbits(b, start + 3, 3);
    *end = start + 6;
    DBGPRINT("-- version %d typeid %d\n", *version, *typeid);
    printf("-- version %d typeid %d\n", *version, *typeid);

    if(version_sum)
        *version_sum += *version;
    return 0;
}

unsigned long parse_literal(int * end, struct bitvector * b, int start)
{
    unsigned long retval = 0;
    int continuation;
    int position = start;

    /* read series of 5 bits until we get one that doesn't start with 1 */
    do {
        continuation = getbits(b, position, 1);
        retval = (retval << 4) | getbits(b, position + 1, 4);
        position += 5;
    } while(continuation);
    *end = position;
    return retval;
}

void parse_operator_length(struct bitvector * b, int * end, int start,
        int * subpacket_length, int * nsubpackets)
{
    int lengthTypeId;
    int position = start;

    /* parse length type ID */
    lengthTypeId = getbits(b, position, 1);
    position++;
    if(0 == lengthTypeId)
    {
        *subpacket_length = getbits(b, position, 15);
        *nsubpackets = 0;
        position += 15;
    }
    else
    {
        *subpacket_length = 0;
        *nsubpackets = getbits(b, position, 11);
        position += 11;
    }

    *end = position;
}

unsigned long parse_operator(struct bitvector * b, int * end,
        int * version_sum, int start,
        int operator_typeid, int subpacket_length, int nsubpackets)
{
    int npackets_parsed = 0;
    unsigned long value = 0, next_value;
    int next_version, next_typeid, next_subpacket_length, next_nsubpackets;
    int position = start;

printf("(");
    /* initialize value */
    switch(operator_typeid) {
        case 0: /* sum */
printf("+");
            value = 0;
            break;
        case 1: /* produuct */
printf("*");
            value = 1;
            break;
        case 2: /* min */
printf("min");
            value = 0xffffffff;
            break;
        case 3: /* max */
printf("max");
            value = 0;
            break;
        default:
            break;
    }

    for(npackets_parsed = 0;
            (nsubpackets && (npackets_parsed < nsubpackets)) ||
            (subpacket_length && (position - start < subpacket_length));
        npackets_parsed++)
    {
        parse_header(&next_version, &next_typeid, &position, version_sum, b,
                position);

        /* parse next value */
        if(4 == next_typeid)  /* literal */
        {
            next_value = parse_literal(&position, b, position);
printf("%lu,", next_value);
        }
        else
        {
            parse_operator_length(b, &position, position,
                    &next_subpacket_length, &next_nsubpackets);
            next_value = parse_operator(b, &position, version_sum, position,
                    next_typeid, next_subpacket_length, next_nsubpackets);
        }

        /* do something with next value */
        switch(operator_typeid) {
            case 0: /* sum */
                value += next_value;
                break;
            case 1: /* product */
                value *= next_value;
                break;
            case 2: /* minimum */
                if(0 == npackets_parsed)
                {
                    /* first value parsed. Take this one */
                    value = next_value;
                }
                else
                {
                    if(next_value < value)
                        value = next_value;
                }
                break;
            case 3: /* maximum */
                if(0 == npackets_parsed)
                {
                    /* first value parsed. Take this one */
                    value = next_value;
                }
                else
                {
                    if(next_value > value)
                        value = next_value;
                }
                break;
            case 4: /* literal */
                value = next_value;
printf("%lu,", value);
                break;
            case 5: /* greater than */
                if(0 == npackets_parsed)
                {
                    /* just preserve this value */
                    value = next_value;
                }
                else
                {
printf("%lu > %lu", value, next_value);
                    if(value > next_value)
                        value = 1;
                    else
                        value = 0;
                }
                break;
            case 6: /* less than */
                if(0 == npackets_parsed)
                {
                    /* just preserve this value */
                    value = next_value;
                }
                else
                {
printf("%lu < %lu", value, next_value);
                    if(value < next_value)
                        value = 1;
                    else
                        value = 0;
                }
                break;
            case 7: /* equal to */
                if(0 == npackets_parsed)
                {
                    /* just preserve this value */
                    value = next_value;
                }
                else
                {
printf("%lu = %lu", value, next_value);
                    if(value == next_value)
                        value = 1;
                    else
                        value = 0;
                }
                break;
        }
    }
    if(end)
        *end = position;
printf(")");

    return value;
}


unsigned long parse_packets(struct bitvector * b, int * version_sum)
{
    int version, typeid, position;
    int subpacket_length, nsubpackets;
    unsigned long value;

    DBGPRINT("----- starting parse\n");

    for(position = 0;
            position < b->length;
            )
    {
        /* parse header for this packet */
        parse_header(&version, &typeid, &position, version_sum, b, position);
        DBGPRINT("  Found packet version %d typeid %d\n", version, typeid);

        if(4 == typeid)
        {
            DBGPRINT("top-level literal\n");
            /* literal */
            value = parse_literal(&position, b, position);
printf("%lu,",value);
        }
        else
        {
            DBGPRINT("top-level operator, version %d typeid %d\n", version, typeid);
            /* operator packet. Check length type ID */
            parse_operator_length(b, &position, position,
                    &subpacket_length, &nsubpackets);
            /* parse operator subpackets */
            value = parse_operator(b, &position, version_sum, position,
                    typeid, subpacket_length, nsubpackets);
        }
        DBGPRINT("ending packet parse, position now %d\n", position);
    }
    printf("\n");

    return value;
}


int main(int argc, char ** argv)
{
#ifdef TEST
    test();
    int version_sum;
    struct bitvector literal = {
        "\xD2\xFE\x28", 21 };
    version_sum = 0;
    parse_packets(&literal, &version_sum);
    if(version_sum != 6)
    {
        printf("ERROR: couldn't parse test literal, expected version sum 6,"
                " received %d\n", version_sum);
    }

    struct bitvector operator = {
        { 0x38, 0x00, 0x6F, 0x45, 0x29, 0x12, 0x00 }, 49 };
    version_sum = 0;
    parse_packets(&operator, &version_sum);
    if(version_sum != 9)
    {
        printf("ERROR: couldn't parse test operator, expected version sum 9,"
                " received %d\n", version_sum);
    }

    struct bitvector operator2 = {
        { 0xEE, 0x00, 0xD4, 0x0C, 0x82, 0x30, 0x60 }, 51 };
    version_sum = 0;
    parse_packets(&operator2, &version_sum);
    if(version_sum != 14)
    {
        printf("ERROR: couldn't parse test operator2, expected version sum 14,"
                " received %d\n", version_sum);
    }

    struct bitvector test1 = {
        { 0x8A, 0x00, 0x4A, 0x80, 0x1A, 0x80, 0x02, 0xF4, 0x78 }, 69 };
    version_sum = 0;
    parse_packets(&test1, &version_sum);
    if(version_sum != 16)
    {
        printf("ERROR: couldn't parse test 1, expected version sum 14,"
                " received %d\n", version_sum);
    }

    struct bitvector test2 = {
        { 0x62, 0x00, 0x80, 0x00, 0x16, 0x11, 0x56, 0x2C, 0x88, 0x02, 0x11,
            0x8E, 0x34 }, 13 * 8 - 2 };
    version_sum = 0;
    parse_packets(&test2, &version_sum);
    if(version_sum != 12)
    {
        printf("ERROR: couldn't parse test 2, expected version sum 12,"
                " received %d\n", version_sum);
    }

    struct bitvector test3 = {
        { 0xC0, 0x01, 0x50, 0x00, 0x01, 0x61, 0x15, 0xA2, 0xE0, 0x80, 0x2F,
            0x18, 0x23, 0x40 }, 14 * 8 - 6 };
    version_sum = 0;
    parse_packets(&test3, &version_sum);
    if(version_sum != 23)
    {
        printf("ERROR: couldn't parse test 3, expected version sum 23,"
                " received %d\n", version_sum);
    }

    struct bitvector test4 = {
        { 0xA0, 0x01, 0x6C, 0x88, 0x01, 0x62, 0x01, 0x7C, 0x36, 0x86, 0xB1,
            0x8A, 0x3D, 0x47, 0x80 }, 15 * 8 - 7};
    version_sum = 0;
    parse_packets(&test4, &version_sum);
    if(version_sum != 31)
    {
        printf("ERROR: couldn't parse test 4, expected version sum 31,"
                " received %d\n", version_sum);
    }
#elif defined(TEST2)
    unsigned long value;
    struct bitvector test2_0 = {
        { 0xC2,0x00,0xB4,0x0A,0x82 }, 5*8};
    value = parse_packets(&test2_0, NULL);
    if(value != 3)
    {
        printf("ERROR: test2_0, value %lu, expected %d\n",
                value, 3);
    }

    struct bitvector test2_1 = {
        { 0x04,0x00,0x5A,0xC3,0x38,0x90, }, 44 };
    value = parse_packets(&test2_1, NULL);
    if(value != 54)
    {
        printf("ERROR: test2_1, value %lu, expected %d\n",
                value, 54);
    }

    struct bitvector test2_2 = {
        { 0x88,0x00,0x86,0xC3,0xE8,0x81,0x12 }, 55 };
    value = parse_packets(&test2_2, NULL);
    if(value != 7)
    {
        printf("ERROR: test2_2, value %lu, expected %d\n",
                value, 7);
    }

    /* 
    CE00C43D881120
    11001110000000001100010000111101100010000001000100100000
    110 011 1 00000000011
     000 100 00111
     101 100 01000
     000 100 01001
    */
    struct bitvector test2_3 = {
        { 0xCE,0x00,0xC4,0x3D,0x88,0x11,0x20 }, 51 };
    value = parse_packets(&test2_3, NULL);
    if(value != 9)
    {
        printf("ERROR: test2_3, value %lu, expected %d\n",
                value, 9);
    }

    struct bitvector test2_4 = {
        { 0xD8,0x00,0x5A,0xC2,0xA8,0xF0 }, 44 };
    value = parse_packets(&test2_4, NULL);
    if(value != 1)
    {
        printf("ERROR: test2_4, value %lu, expected %d\n",
                value, 1);
    }

    /* F600BC2D8F
     * 1111011000000000101111000010110110001111
     * 111 101 1 00000000010
     *  111 100 00101
     *  101 100 01111 */
    struct bitvector test2_5 = {
        { 0xF6,0x00,0xBC,0x2D,0x8F }, 5*8 };
    value = parse_packets(&test2_5, NULL);
    if(value != 0)
    {
        printf("ERROR: test2_5, value %lu, expected %d\n",
                value, 0);
    }

    struct bitvector test2_6 = {
        { 0x9C,0x00,0x5A,0xC2,0xF8,0xF0 }, 44 };
    value = parse_packets(&test2_6, NULL);
    if(value != 0)
    {
        printf("ERROR: test2_6, value %lu, expected %d\n",
                value, 0);
    }

    /* 9C0141080250320F1802104A08
     * 10011100000000010100000100001000000000100101000000110010000011110001100000000010000100000100101000001000
     * 100 111 0 000000001010000
     *  010 000 1 00000000010
     *   010 100 00001
     *   100 100 00011
     *  110 001 1 00000000010
     *   000 100 00010
     *   010 100 00010 */
    struct bitvector test2_7 = {
        { 0x9C,0x01,0x41,0x08,0x02,0x50,0x32,0x0F,0x18,0x02,0x10,0x4A,0x08 }, 102 };
    value = parse_packets(&test2_7, NULL);
    if(value != 1)
    {
        printf("ERROR: test2_7, value %lu, expected %d\n",
                value, 1);
    }

#else  /* not TEST */
    struct bitvector b = {
        { 0x00,0x54,0x10,0xC9,0x9A,0x98,0x02,0xDA,0x00,0xB4,0x38,0x87,0x13,0x8F,0x72,0xF4,0xF6,0x52,0xCC,0x01,0x59,0xFE,0x05,0xE8,0x02,0xB3,0xA5,0x72,0xDB,0xBE,0x5A,0xA5,0xF5,0x6F,0x6B,0x6A,0x46,0x00,0xFC,0xCA,0xAC,0xEA,0x9C,0xE0,0xE1,0x00,0x20,0x13,0xA5,0x53,0x89,0xB0,0x64,0xC0,0x26,0x98,0x13,0x95,0x2F,0x98,0x35,0x95,0x23,0x40,0x02,0xDA,0x39,0x46,0x15,0x00,0x2A,0x47,0xE0,0x6C,0x01,0x25,0xCF,0x7B,0x74,0xFE,0x00,0xE6,0xFC,0x47,0x0D,0x4C,0x01,0x29,0x26,0x0B,0x00,0x5E,0x73,0xFC,0xDF,0xC3,0xA5,0xB7,0x7B,0xF2,0xFB,0x4E,0x00,0x09,0xC2,0x7E,0xCE,0xF2,0x93,0x82,0x4C,0xC7,0x69,0x02,0xB3,0x00,0x4F,0x80,0x17,0xA9,0x99,0xEC,0x22,0x77,0x04,0x12,0xBE,0x2A,0x10,0x04,0xE3,0xDC,0xDF,0xA1,0x46,0xD0,0x00,0x20,0x67,0x0B,0x9C,0x01,0x29,0xA8,0xD7,0x9B,0xB7,0xE8,0x89,0x26,0xBA,0x40,0x1B,0xAD,0x00,0x48,0x92,0xBB,0xDE,0xF2,0x0D,0x25,0x3B,0xE7,0x0C,0x53,0xCA,0x53,0x99,0xAB,0x64,0x8E,0xBB,0xAA,0xF0,0xBD,0x40,0x2B,0x95,0x34,0x92,0x01,0x93,0x82,0x64,0xC7,0x69,0x9C,0x5A,0x05,0x92,0xAF,0x80,0x01,0xE3,0xC0,0x99,0x72,0xA9,0x49,0xAD,0x4A,0xE2,0xCB,0x32,0x30,0xAC,0x37,0xFC,0x91,0x98,0x01,0xF2,0xA7,0xA4,0x02,0x97,0x80,0x02,0x15,0x0E,0x60,0xBC,0x67,0x00,0x04,0x3A,0x23,0xC6,0x18,0xE2,0x00,0x08,0x64,0x47,0x82,0xF1,0x0C,0x80,0x26,0x2F,0x00,0x56,0x79,0xA6,0x79,0xBE,0x73,0x3C,0x3F,0x30,0x05,0xBC,0x01,0x49,0x6F,0x60,0x86,0x5B,0x39,0xAF,0x8A,0x24,0x78,0xA0,0x40,0x17,0xDC,0xBE,0xAB,0x32,0xFA,0x00,0x55,0xE6,0x28,0x6D,0x31,0x43,0x03,0x00,0xAE,0x7C,0x7E,0x79,0xAE,0x55,0x32,0x4C,0xA6,0x79,0xF9,0x00,0x22,0x39,0x99,0x2B,0xC6,0x89,0xA8,0xD6,0xFE,0x08,0x40,0x12,0xAE,0x73,0xBD,0xFE,0x39,0xEB,0xF1,0x86,0x73,0x8B,0x33,0xBD,0x9F,0xA9,0x1B,0x14,0xCB,0x77,0x85,0xEC,0x01,0xCE,0x4D,0xCE,0x1A,0xE2,0xDC,0xFD,0x7D,0x23,0x09,0x8A,0x98,0x41,0x19,0x73,0xE3,0x00,0x52,0xC0,0x12,0x97,0x8F,0x7D,0xD0,0x89,0x68,0x9A,0xCD,0x4A,0x7A,0x80,0xCC,0xEF,0xEB,0x9E,0xC5,0x68,0x80,0x48,0x59,0x51,0xDB,0x00,0x40,0x00,0x10,0xD8,0xA3,0x0C,0xA1,0x50,0x00,0x21,0xB0,0xD6,0x25,0x45,0x07,0x00,0x22,0x7A,0x30,0xA7,0x74,0xB2,0x60,0x0A,0xCD,0x56,0xF9,0x81,0xE5,0x80,0x27,0x2A,0xA3,0x31,0x9A,0xCC,0x04,0xC0,0x15,0xC0,0x0A,0xFA,0x46,0x16,0xC6,0x3D,0x4D,0xFF,0x28,0x93,0x19,0xA9,0xDC,0x40,0x10,0x08,0x65,0x09,0x27,0xB2,0x23,0x2F,0x70,0x78,0x4A,0xE0,0x12,0x4D,0x65,0xA2,0x5F,0xD3,0xA3,0x4C,0xC6,0x1A,0x64,0x49,0x24,0x69,0x86,0xE3,0x00,0x42,0x5A,0xF8,0x73,0xA0,0x0C,0xD4,0x40,0x1C,0x8A,0x90,0xD6,0x0E,0x88,0x03,0xD0,0x8A,0x0D,0xC6,0x73,0x00,0x5E,0x69,0x2B,0x00,0x0D,0xA8,0x5B,0x26,0x8E,0x40,0x21,0xD4,0xE4,0x1C,0x68,0x02,0xE4,0x9A,0xB5,0x7D,0x1E,0xD1,0x16,0x6A,0xD5,0xF4,0x7B,0x44,0x33,0x00,0x5F,0x40,0x14,0x96,0x86,0x7C,0x2B,0x3E,0x71,0x12,0xC0,0x05,0x0C,0x20,0x04,0x3A,0x17,0xC2,0x08,0xB2,0x40,0x08,0x74,0x25,0x87,0x11,0x80,0xC0,0x19,0x85,0xD0,0x7A,0x22,0x98,0x02,0x73,0x24,0x78,0x01,0x98,0x88,0x03,0xB0,0x8A,0x2D,0xC1,0x91,0x00,0x6A,0x21,0x41,0x28,0x96,0x40,0x13,0x3E,0x80,0x21,0x2C,0x3D,0x2C,0x3F,0x37,0x7B,0x09,0x90,0x0A,0x53,0xE0,0x09,0x00,0x02,0x11,0x09,0x62,0x34,0x25,0x10,0x07,0x23,0xDC,0x68,0x84,0xD3,0xB7,0xCF,0xE1,0xD2,0xC6,0x03,0x6D,0x18,0x0D,0x05,0x30,0x02,0x88,0x0B,0xC5,0x30,0x02,0x5C,0x00,0xF7,0x00,0x30,0x80,0x96,0x11,0x00,0x21,0xC0,0x0C,0x00,0x1E,0x44,0xC0,0x0F,0x00,0x19,0x55,0x80,0x5A,0x62,0x01,0x3D,0x04,0x00,0xB4,0x00,0xED,0x50,0x03,0x07,0x40,0x09,0x49,0xC0,0x0F,0x92,0x97,0x2B,0x6B,0xC3,0xF4,0x7A,0x96,0xD2,0x1C,0x57,0x30,0x04,0x70,0x03,0x77,0x00,0x04,0x32,0x3E,0x44,0xF8,0xB8,0x00,0x08,0x44,0x1C,0x8F,0x51,0x36,0x6F,0x38,0xF2,0x40}, 1353 * 4 - 10};
    int version_sum = 0;
    unsigned long value;
    value = parse_packets(&b, &version_sum);
    printf("Version sum: %d\n", version_sum);
    printf("Value: %lu\n", value);
#endif

    return 0;
}

