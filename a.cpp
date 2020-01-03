#ifndef MC_TEST
#define MC_TEST

//#define DATA  {0,0,100,23}
#define CHARDATA  {'a', {'b'}, 23}
// #define STRDATA  {"god", "(hi),{how are [you]?}", ",", {"inner_{1}",{"inner_{2}", "inner_{2}_(1)"}}}

 /*test*/ #define /*middle_1***/ COMSTRUCT /*middle_2*/ { {1, 2.0, "str"}, {'1', .0075e1f,  /*test*/ "\\\\\\\\\\\\\\\\\\//////////////////"},   /*test*/ { +0x1dCbAF, 1.2E+0,  /*""*/ "\v\'\"\f \"\n\r\t\b\a\\",},}  /*enddd*/ //end

#define special "'1~!@#$^&*()_+-={':[,]}|;.</>?"
  
#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"

#define c_hex '\x0c'
#define c_oct '\12'
#define c_squote '\''
#define c_quote '\"'
#define c_bell '\a'
#define c_back '\b'
#define c_formfeed '\f'
#define c_htab '\t'
#define c_vtab '\v'
#define c_bslash '\\'
#define c_newline '\n'

#define HEX_A -0xa4A8
#define HEX_B 0X3fdB9
#define HEX_C 0X4f3L

#define quote '"'
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define slash "/ &^ \\"
#define _wide_str L"This is a string literal."//wide string "This is a string literal."

#define splitstr "24'23't" "323df" //"123fg"
#define comment/*I am a comment!*/"// /* */<!-- --"


//comment/*test*//
/*comment//test*/

#define trap "#define AA 123"

#define backslash	'\\'
#define tab_		'\t'

#define NS1 "with tab	"    
#define NSRT "XXX \\tYYY\\nZZZZ \\n"

#define testE 25E-4
#define testE1 -1.5E-4

#define long_double  100.0L
#define float_only 100.2F
#define decimal_only .0075 
#define unsigned_intn 123u

#define long_unsigned_intn 776255UL
#define long_intn 4293955295L /* /*     
//Stringizing Operator  (#) 
#define stringer( x ) printf_s( #x "\\n" )

#define _X 0200
#define _Y 1234
//#define F abc/
#define B def

#define DATA  {210,41,78.0,323,-457}

/* */
# /*321*/ define TT 123123
/* 
comment */#define _1X 32.0
#define _1Y -48.970
#define _XY {-23,41}
#define _X 0100 //0ctal /* Constants
#define _Y -0124

#define COMPDATA  { {1,3, {2,3,5}, {31} },  {{12,016}, {1,30,0}}, 23 }


#else

#endif // !MC_TEST