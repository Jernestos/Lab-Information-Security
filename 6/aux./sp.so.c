typedef unsigned char   undefined;

typedef unsigned char    byte;
typedef unsigned char    dwfenc;
typedef unsigned int    dword;
typedef long long    longlong;
typedef unsigned long    qword;
typedef long    sqword;
typedef unsigned char    uchar;
typedef unsigned int    uint;
typedef unsigned long    ulong;
typedef unsigned long long    ulonglong;
typedef unsigned char    undefined1;
typedef unsigned int    undefined4;
typedef unsigned long    undefined8;
typedef unsigned short    ushort;
typedef unsigned short    word;
typedef struct eh_frame_hdr eh_frame_hdr, *Peh_frame_hdr;

struct eh_frame_hdr {
    byte eh_frame_hdr_version; // Exception Handler Frame Header Version
    dwfenc eh_frame_pointer_encoding; // Exception Handler Frame Pointer Encoding
    dwfenc eh_frame_desc_entry_count_encoding; // Encoding of # of Exception Handler FDEs
    dwfenc eh_frame_table_encoding; // Exception Handler Table Encoding
};

typedef struct fde_table_entry fde_table_entry, *Pfde_table_entry;

struct fde_table_entry {
    dword initial_loc; // Initial Location
    dword data_loc; // Data location
};

typedef void _IO_lock_t;

typedef struct _IO_marker _IO_marker, *P_IO_marker;

typedef struct _IO_FILE _IO_FILE, *P_IO_FILE;

typedef long __off_t;

typedef long __off64_t;

typedef ulong size_t;

struct _IO_FILE {
    int _flags;
    char * _IO_read_ptr;
    char * _IO_read_end;
    char * _IO_read_base;
    char * _IO_write_base;
    char * _IO_write_ptr;
    char * _IO_write_end;
    char * _IO_buf_base;
    char * _IO_buf_end;
    char * _IO_save_base;
    char * _IO_backup_base;
    char * _IO_save_end;
    struct _IO_marker * _markers;
    struct _IO_FILE * _chain;
    int _fileno;
    int _flags2;
    __off_t _old_offset;
    ushort _cur_column;
    char _vtable_offset;
    char _shortbuf[1];
    _IO_lock_t * _lock;
    __off64_t _offset;
    void * __pad1;
    void * __pad2;
    void * __pad3;
    void * __pad4;
    size_t __pad5;
    int _mode;
    char _unused2[20];
};

struct _IO_marker {
    struct _IO_marker * _next;
    struct _IO_FILE * _sbuf;
    int _pos;
};

typedef qword __uint64_t;


// WARNING! conflicting data type names: /DWARF/uchar - /uchar


// WARNING! conflicting data type names: /DWARF/__off64_t - /types.h/__off64_t

typedef long __ssize_t;

typedef ulong __re_long_size_t;

typedef dword __uint32_t;

typedef ulong reg_syntax_t;


// WARNING! conflicting data type names: /DWARF/uint - /uint

typedef uchar __uint8_t;

typedef __ssize_t ssize_t;

typedef ssize_t Py_ssize_t;

typedef Py_ssize_t Py_hash_t;

typedef struct _PyTraceMalloc_Config _PyTraceMalloc_Config, *P_PyTraceMalloc_Config;

typedef enum anon_enum_32.conflict486 {
    TRACEMALLOC_NOT_INITIALIZED=0,
    TRACEMALLOC_INITIALIZED=1,
    TRACEMALLOC_FINALIZED=2
} anon_enum_32.conflict486;

struct _PyTraceMalloc_Config {
    enum anon_enum_32.conflict486 initialized;
    int tracing;
    int max_nframe;
    int use_domain;
};

typedef union _Py_HashSecret_t _Py_HashSecret_t, *P_Py_HashSecret_t;

typedef struct anon_struct_16_2_1b672598_for_fnv anon_struct_16_2_1b672598_for_fnv, *Panon_struct_16_2_1b672598_for_fnv;

typedef struct anon_struct_16_2_f9f05f3a_for_siphash anon_struct_16_2_f9f05f3a_for_siphash, *Panon_struct_16_2_f9f05f3a_for_siphash;

typedef struct anon_struct_24_2_1649c6a0_for_djbx33a anon_struct_24_2_1649c6a0_for_djbx33a, *Panon_struct_24_2_1649c6a0_for_djbx33a;

typedef struct anon_struct_24_2_9bb791b3_for_expat anon_struct_24_2_9bb791b3_for_expat, *Panon_struct_24_2_9bb791b3_for_expat;

typedef __uint64_t uint64_t;

struct anon_struct_16_2_f9f05f3a_for_siphash {
    uint64_t k0;
    uint64_t k1;
};

struct anon_struct_24_2_9bb791b3_for_expat {
    uchar padding[16];
    Py_hash_t hashsalt;
};

struct anon_struct_24_2_1649c6a0_for_djbx33a {
    uchar padding[16];
    Py_hash_t suffix;
};

struct anon_struct_16_2_1b672598_for_fnv {
    Py_hash_t prefix;
    Py_hash_t suffix;
};

union _Py_HashSecret_t {
    uchar uc[24];
    struct anon_struct_16_2_1b672598_for_fnv fnv;
    struct anon_struct_16_2_f9f05f3a_for_siphash siphash;
    struct anon_struct_24_2_1649c6a0_for_djbx33a djbx33a;
    struct anon_struct_24_2_9bb791b3_for_expat expat;
};

typedef struct _inittab _inittab, *P_inittab;

typedef struct _object _object, *P_object;

typedef struct _object PyObject;

typedef struct _typeobject _typeobject, *P_typeobject;


// WARNING! conflicting data type names: /DWARF/struct_FILE.h/_IO_FILE - /stdio.h/_IO_FILE

typedef struct _IO_FILE FILE;

typedef struct PyVarObject PyVarObject, *PPyVarObject;

typedef void (* destructor)(PyObject *);

typedef PyObject * (* getattrfunc)(PyObject *, char *);

typedef int (* setattrfunc)(PyObject *, char *, PyObject *);

typedef struct PyAsyncMethods PyAsyncMethods, *PPyAsyncMethods;

typedef PyObject * (* reprfunc)(PyObject *);

typedef struct PyNumberMethods PyNumberMethods, *PPyNumberMethods;

typedef struct PySequenceMethods PySequenceMethods, *PPySequenceMethods;

typedef struct PyMappingMethods PyMappingMethods, *PPyMappingMethods;

typedef Py_hash_t (* hashfunc)(PyObject *);

typedef PyObject * (* ternaryfunc)(PyObject *, PyObject *, PyObject *);

typedef PyObject * (* getattrofunc)(PyObject *, PyObject *);

typedef int (* setattrofunc)(PyObject *, PyObject *, PyObject *);

typedef struct PyBufferProcs PyBufferProcs, *PPyBufferProcs;

typedef int (* visitproc)(PyObject *, void *);

typedef int (* traverseproc)(PyObject *, visitproc, void *);

typedef int (* inquiry)(PyObject *);

typedef PyObject * (* richcmpfunc)(PyObject *, PyObject *, int);

typedef PyObject * (* getiterfunc)(PyObject *);

typedef PyObject * (* iternextfunc)(PyObject *);

typedef struct PyMethodDef PyMethodDef, *PPyMethodDef;

typedef struct PyMemberDef PyMemberDef, *PPyMemberDef;

typedef struct PyGetSetDef PyGetSetDef, *PPyGetSetDef;

typedef PyObject * (* descrgetfunc)(PyObject *, PyObject *, PyObject *);

typedef int (* descrsetfunc)(PyObject *, PyObject *, PyObject *);

typedef int (* initproc)(PyObject *, PyObject *, PyObject *);

typedef PyObject * (* allocfunc)(struct _typeobject *, Py_ssize_t);

typedef PyObject * (* newfunc)(struct _typeobject *, PyObject *, PyObject *);

typedef void (* freefunc)(void *);

typedef PyObject * (* vectorcallfunc)(PyObject *, PyObject * *, size_t, PyObject *);

typedef PyObject * (* unaryfunc)(PyObject *);

typedef PyObject * (* binaryfunc)(PyObject *, PyObject *);

typedef Py_ssize_t (* lenfunc)(PyObject *);

typedef PyObject * (* ssizeargfunc)(PyObject *, Py_ssize_t);

typedef int (* ssizeobjargproc)(PyObject *, Py_ssize_t, PyObject *);

typedef int (* objobjproc)(PyObject *, PyObject *);

typedef int (* objobjargproc)(PyObject *, PyObject *, PyObject *);

typedef struct bufferinfo bufferinfo, *Pbufferinfo;

typedef struct bufferinfo Py_buffer;

typedef int (* getbufferproc)(PyObject *, Py_buffer *, int);

typedef void (* releasebufferproc)(PyObject *, Py_buffer *);

typedef PyObject * (* PyCFunction)(PyObject *, PyObject *);

typedef PyObject * (* getter)(PyObject *, void *);

typedef int (* setter)(PyObject *, PyObject *, void *);

struct PyMemberDef {
};

struct bufferinfo {
    void * buf;
    PyObject * obj;
    Py_ssize_t len;
    Py_ssize_t itemsize;
    int readonly;
    int ndim;
    char * format;
    Py_ssize_t * shape;
    Py_ssize_t * strides;
    Py_ssize_t * suboffsets;
    void * internal;
};

struct PyGetSetDef {
    char * name;
    getter get;
    setter set;
    char * doc;
    void * closure;
};

struct PyAsyncMethods {
    unaryfunc am_await;
    unaryfunc am_aiter;
    unaryfunc am_anext;
};

struct _object {
    Py_ssize_t ob_refcnt;
    struct _typeobject * ob_type;
};

struct PyVarObject {
    PyObject ob_base;
    Py_ssize_t ob_size;
};

struct _typeobject {
    struct PyVarObject ob_base;
    char * tp_name;
    Py_ssize_t tp_basicsize;
    Py_ssize_t tp_itemsize;
    destructor tp_dealloc;
    Py_ssize_t tp_vectorcall_offset;
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    struct PyAsyncMethods * tp_as_async;
    reprfunc tp_repr;
    struct PyNumberMethods * tp_as_number;
    struct PySequenceMethods * tp_as_sequence;
    struct PyMappingMethods * tp_as_mapping;
    hashfunc tp_hash;
    ternaryfunc tp_call;
    reprfunc tp_str;
    getattrofunc tp_getattro;
    setattrofunc tp_setattro;
    struct PyBufferProcs * tp_as_buffer;
    ulong tp_flags;
    char * tp_doc;
    traverseproc tp_traverse;
    inquiry tp_clear;
    richcmpfunc tp_richcompare;
    Py_ssize_t tp_weaklistoffset;
    getiterfunc tp_iter;
    iternextfunc tp_iternext;
    struct PyMethodDef * tp_methods;
    struct PyMemberDef * tp_members;
    struct PyGetSetDef * tp_getset;
    struct _typeobject * tp_base;
    PyObject * tp_dict;
    descrgetfunc tp_descr_get;
    descrsetfunc tp_descr_set;
    Py_ssize_t tp_dictoffset;
    initproc tp_init;
    allocfunc tp_alloc;
    newfunc tp_new;
    freefunc tp_free;
    inquiry tp_is_gc;
    PyObject * tp_bases;
    PyObject * tp_mro;
    PyObject * tp_cache;
    PyObject * tp_subclasses;
    PyObject * tp_weaklist;
    destructor tp_del;
    uint tp_version_tag;
    destructor tp_finalize;
    vectorcallfunc tp_vectorcall;
    int (* tp_print)(PyObject *, FILE *, int);
};

struct PyNumberMethods {
    binaryfunc nb_add;
    binaryfunc nb_subtract;
    binaryfunc nb_multiply;
    binaryfunc nb_remainder;
    binaryfunc nb_divmod;
    ternaryfunc nb_power;
    unaryfunc nb_negative;
    unaryfunc nb_positive;
    unaryfunc nb_absolute;
    inquiry nb_bool;
    unaryfunc nb_invert;
    binaryfunc nb_lshift;
    binaryfunc nb_rshift;
    binaryfunc nb_and;
    binaryfunc nb_xor;
    binaryfunc nb_or;
    unaryfunc nb_int;
    void * nb_reserved;
    unaryfunc nb_float;
    binaryfunc nb_inplace_add;
    binaryfunc nb_inplace_subtract;
    binaryfunc nb_inplace_multiply;
    binaryfunc nb_inplace_remainder;
    ternaryfunc nb_inplace_power;
    binaryfunc nb_inplace_lshift;
    binaryfunc nb_inplace_rshift;
    binaryfunc nb_inplace_and;
    binaryfunc nb_inplace_xor;
    binaryfunc nb_inplace_or;
    binaryfunc nb_floor_divide;
    binaryfunc nb_true_divide;
    binaryfunc nb_inplace_floor_divide;
    binaryfunc nb_inplace_true_divide;
    unaryfunc nb_index;
    binaryfunc nb_matrix_multiply;
    binaryfunc nb_inplace_matrix_multiply;
};

struct PyBufferProcs {
    getbufferproc bf_getbuffer;
    releasebufferproc bf_releasebuffer;
};

struct PyMappingMethods {
    lenfunc mp_length;
    binaryfunc mp_subscript;
    objobjargproc mp_ass_subscript;
};

struct PyMethodDef {
    char * ml_name;
    PyCFunction ml_meth;
    int ml_flags;
    char * ml_doc;
};

struct _inittab {
    char * name;
    PyObject * (* initfunc)(void);
};

struct PySequenceMethods {
    lenfunc sq_length;
    binaryfunc sq_concat;
    ssizeargfunc sq_repeat;
    ssizeargfunc sq_item;
    void * was_sq_slice;
    ssizeobjargproc sq_ass_item;
    void * was_sq_ass_slice;
    objobjproc sq_contains;
    binaryfunc sq_inplace_concat;
    ssizeargfunc sq_inplace_repeat;
};

typedef struct _frozen _frozen, *P_frozen;

struct _frozen {
    char * name;
    uchar * code;
    int size;
};

typedef struct aes_context aes_context, *Paes_context;

typedef __uint32_t uint32_t;

struct aes_context {
    int mode;
    int rounds;
    uint32_t * rk;
    uint32_t buf[68];
};

typedef struct gcm_context gcm_context, *Pgcm_context;

struct gcm_context {
    int mode;
    uint64_t len;
    uint64_t add_len;
    uint64_t HL[16];
    uint64_t HH[16];
    uchar base_ectr[16];
    uchar y[16];
    uchar buf[16];
    struct aes_context aes_ctx;
};

typedef struct _typeobject PyTypeObject;

typedef struct _IO_wide_data _IO_wide_data, *P_IO_wide_data;

struct _IO_wide_data {
};


// WARNING! conflicting data type names: /DWARF/_UNCATEGORIZED_/_IO_marker - /libio.h/_IO_marker

typedef struct _IO_codecvt _IO_codecvt, *P_IO_codecvt;

struct _IO_codecvt {
};

typedef struct _frame _frame, *P_frame;

struct _frame {
};

typedef struct re_dfa_t re_dfa_t, *Pre_dfa_t;

struct re_dfa_t {
};

typedef struct _is _is, *P_is;

struct _is {
};

typedef struct _ts _ts, *P_ts;

typedef struct _ts PyThreadState;

typedef struct _is PyInterpreterState;

typedef int (* Py_tracefunc)(PyObject *, struct _frame *, int, PyObject *);

typedef struct _err_stackitem _err_stackitem, *P_err_stackitem;

typedef struct _err_stackitem _PyErr_StackItem;

struct _err_stackitem {
    PyObject * exc_type;
    PyObject * exc_value;
    PyObject * exc_traceback;
    struct _err_stackitem * previous_item;
};

struct _ts {
    struct _ts * prev;
    struct _ts * next;
    PyInterpreterState * interp;
    struct _frame * frame;
    int recursion_depth;
    char overflowed;
    char recursion_critical;
    int stackcheck_counter;
    int tracing;
    int use_tracing;
    Py_tracefunc c_profilefunc;
    Py_tracefunc c_tracefunc;
    PyObject * c_profileobj;
    PyObject * c_traceobj;
    PyObject * curexc_type;
    PyObject * curexc_value;
    PyObject * curexc_traceback;
    _PyErr_StackItem exc_state;
    _PyErr_StackItem * exc_info;
    PyObject * dict;
    int gilstate_counter;
    PyObject * async_exc;
    ulong thread_id;
    int trash_delete_nesting;
    PyObject * trash_delete_later;
    void (* on_delete)(void *);
    void * on_delete_data;
    int coroutine_origin_tracking_depth;
    PyObject * async_gen_firstiter;
    PyObject * async_gen_finalizer;
    PyObject * context;
    uint64_t context_ver;
    uint64_t id;
};

typedef __uint8_t uint8_t;

typedef struct _longobject _longobject, *P_longobject;

typedef uint32_t digit;

struct _longobject {
    struct PyVarObject ob_base;
    digit ob_digit[1];
};

typedef struct re_pattern_buffer re_pattern_buffer, *Pre_pattern_buffer;

struct re_pattern_buffer {
    struct re_dfa_t * buffer;
    __re_long_size_t allocated;
    __re_long_size_t used;
    reg_syntax_t syntax;
    char * fastmap;
    uchar * translate;
    size_t re_nsub;
    uint can_be_null:1;
    uint regs_allocated:2;
    uint fastmap_accurate:1;
    uint no_sub:1;
    uint not_bol:1;
    uint not_eol:1;
    uint newline_anchor:1;
};

typedef struct re_pattern_buffer regex_t;

typedef long __time_t;

typedef __time_t time_t;


// WARNING! conflicting data type names: /stdio.h/FILE - /DWARF/FILE.h/FILE

typedef struct evp_pkey_ctx_st evp_pkey_ctx_st, *Pevp_pkey_ctx_st;

typedef struct evp_pkey_ctx_st EVP_PKEY_CTX;

struct evp_pkey_ctx_st {
};


// WARNING! conflicting data type names: /regex.h/regex_t - /DWARF/regex.h/regex_t

typedef struct regmatch_t regmatch_t, *Pregmatch_t;

typedef int regoff_t;

struct regmatch_t {
    regoff_t rm_so;
    regoff_t rm_eo;
};


// WARNING! conflicting data type names: /regex.h/re_pattern_buffer - /DWARF/regex.h/re_pattern_buffer

typedef enum Elf_ProgramHeaderType {
    PT_NULL=0,
    PT_LOAD=1,
    PT_DYNAMIC=2,
    PT_INTERP=3,
    PT_NOTE=4,
    PT_SHLIB=5,
    PT_PHDR=6,
    PT_TLS=7,
    PT_GNU_EH_FRAME=1685382480,
    PT_GNU_STACK=1685382481,
    PT_GNU_RELRO=1685382482
} Elf_ProgramHeaderType;

typedef struct Elf64_Shdr Elf64_Shdr, *PElf64_Shdr;

typedef enum Elf_SectionHeaderType {
    SHT_NULL=0,
    SHT_PROGBITS=1,
    SHT_SYMTAB=2,
    SHT_STRTAB=3,
    SHT_RELA=4,
    SHT_HASH=5,
    SHT_DYNAMIC=6,
    SHT_NOTE=7,
    SHT_NOBITS=8,
    SHT_REL=9,
    SHT_SHLIB=10,
    SHT_DYNSYM=11,
    SHT_INIT_ARRAY=14,
    SHT_FINI_ARRAY=15,
    SHT_PREINIT_ARRAY=16,
    SHT_GROUP=17,
    SHT_SYMTAB_SHNDX=18,
    SHT_ANDROID_REL=1610612737,
    SHT_ANDROID_RELA=1610612738,
    SHT_GNU_ATTRIBUTES=1879048181,
    SHT_GNU_HASH=1879048182,
    SHT_GNU_LIBLIST=1879048183,
    SHT_CHECKSUM=1879048184,
    SHT_SUNW_move=1879048186,
    SHT_SUNW_COMDAT=1879048187,
    SHT_SUNW_syminfo=1879048188,
    SHT_GNU_verdef=1879048189,
    SHT_GNU_verneed=1879048190,
    SHT_GNU_versym=1879048191
} Elf_SectionHeaderType;

struct Elf64_Shdr {
    dword sh_name;
    enum Elf_SectionHeaderType sh_type;
    qword sh_flags;
    qword sh_addr;
    qword sh_offset;
    qword sh_size;
    dword sh_link;
    dword sh_info;
    qword sh_addralign;
    qword sh_entsize;
};

typedef struct Elf64_Dyn Elf64_Dyn, *PElf64_Dyn;

typedef enum Elf64_DynTag {
    DT_NULL=0,
    DT_NEEDED=1,
    DT_PLTRELSZ=2,
    DT_PLTGOT=3,
    DT_HASH=4,
    DT_STRTAB=5,
    DT_SYMTAB=6,
    DT_RELA=7,
    DT_RELASZ=8,
    DT_RELAENT=9,
    DT_STRSZ=10,
    DT_SYMENT=11,
    DT_INIT=12,
    DT_FINI=13,
    DT_SONAME=14,
    DT_RPATH=15,
    DT_SYMBOLIC=16,
    DT_REL=17,
    DT_RELSZ=18,
    DT_RELENT=19,
    DT_PLTREL=20,
    DT_DEBUG=21,
    DT_TEXTREL=22,
    DT_JMPREL=23,
    DT_BIND_NOW=24,
    DT_INIT_ARRAY=25,
    DT_FINI_ARRAY=26,
    DT_INIT_ARRAYSZ=27,
    DT_FINI_ARRAYSZ=28,
    DT_RUNPATH=29,
    DT_FLAGS=30,
    DT_PREINIT_ARRAY=32,
    DT_PREINIT_ARRAYSZ=33,
    DT_RELRSZ=35,
    DT_RELR=36,
    DT_RELRENT=37,
    DT_ANDROID_REL=1610612751,
    DT_ANDROID_RELSZ=1610612752,
    DT_ANDROID_RELA=1610612753,
    DT_ANDROID_RELASZ=1610612754,
    DT_ANDROID_RELR=1879040000,
    DT_ANDROID_RELRSZ=1879040001,
    DT_ANDROID_RELRENT=1879040003,
    DT_GNU_PRELINKED=1879047669,
    DT_GNU_CONFLICTSZ=1879047670,
    DT_GNU_LIBLISTSZ=1879047671,
    DT_CHECKSUM=1879047672,
    DT_PLTPADSZ=1879047673,
    DT_MOVEENT=1879047674,
    DT_MOVESZ=1879047675,
    DT_FEATURE_1=1879047676,
    DT_POSFLAG_1=1879047677,
    DT_SYMINSZ=1879047678,
    DT_SYMINENT=1879047679,
    DT_GNU_XHASH=1879047924,
    DT_GNU_HASH=1879047925,
    DT_TLSDESC_PLT=1879047926,
    DT_TLSDESC_GOT=1879047927,
    DT_GNU_CONFLICT=1879047928,
    DT_GNU_LIBLIST=1879047929,
    DT_CONFIG=1879047930,
    DT_DEPAUDIT=1879047931,
    DT_AUDIT=1879047932,
    DT_PLTPAD=1879047933,
    DT_MOVETAB=1879047934,
    DT_SYMINFO=1879047935,
    DT_VERSYM=1879048176,
    DT_RELACOUNT=1879048185,
    DT_RELCOUNT=1879048186,
    DT_FLAGS_1=1879048187,
    DT_VERDEF=1879048188,
    DT_VERDEFNUM=1879048189,
    DT_VERNEED=1879048190,
    DT_VERNEEDNUM=1879048191,
    DT_AUXILIARY=2147483645,
    DT_FILTER=2147483647
} Elf64_DynTag;

struct Elf64_Dyn {
    enum Elf64_DynTag d_tag;
    qword d_val;
};

typedef struct Gnu_BuildId Gnu_BuildId, *PGnu_BuildId;

struct Gnu_BuildId {
    dword namesz; // Length of name field
    dword descsz; // Length of description field
    dword type; // Vendor specific type
    char name[4]; // Build-id vendor name
    byte description[20]; // Build-id value
};

typedef struct Elf64_Ehdr Elf64_Ehdr, *PElf64_Ehdr;

struct Elf64_Ehdr {
    byte e_ident_magic_num;
    char e_ident_magic_str[3];
    byte e_ident_class;
    byte e_ident_data;
    byte e_ident_version;
    byte e_ident_osabi;
    byte e_ident_abiversion;
    byte e_ident_pad[7];
    word e_type;
    word e_machine;
    dword e_version;
    qword e_entry;
    qword e_phoff;
    qword e_shoff;
    dword e_flags;
    word e_ehsize;
    word e_phentsize;
    word e_phnum;
    word e_shentsize;
    word e_shnum;
    word e_shstrndx;
};

typedef struct Elf64_Rela Elf64_Rela, *PElf64_Rela;

struct Elf64_Rela {
    qword r_offset; // location to apply the relocation action
    qword r_info; // the symbol table index and the type of relocation
    qword r_addend; // a constant addend used to compute the relocatable field value
};

typedef struct Elf64_Phdr Elf64_Phdr, *PElf64_Phdr;

struct Elf64_Phdr {
    enum Elf_ProgramHeaderType p_type;
    dword p_flags;
    qword p_offset;
    qword p_vaddr;
    qword p_paddr;
    qword p_filesz;
    qword p_memsz;
    qword p_align;
};

typedef struct Elf64_Sym Elf64_Sym, *PElf64_Sym;

struct Elf64_Sym {
    dword st_name;
    byte st_info;
    byte st_other;
    word st_shndx;
    qword st_value;
    qword st_size;
};




int _init(EVP_PKEY_CTX *ctx)

{
  int iVar1;
  
  iVar1 = __gmon_start__();
  return iVar1;
}



void FUN_00102020(void)

{
                    // WARNING: Treating indirect jump as call
  (*(code *)(undefined *)0x0)();
  return;
}



void __cxa_finalize(void)

{
  __cxa_finalize();
  return;
}



void gcm_zero_ctx(gcm_context *ctx)

{
  memset(ctx,0,0x268);
  return;
}



int gcm_finish(gcm_context *ctx,uchar *tag,size_t tag_len)

{
  byte abStack_38 [24];
  long lStack_20;
  long lStack_18;
  ulong uStack_10;
  
  lStack_18 = ctx->len << 3;
  lStack_20 = ctx->add_len << 3;
  if (tag_len != 0) {
    memcpy(tag,ctx->base_ectr,tag_len);
  }
  if ((lStack_18 != 0) || (lStack_20 != 0)) {
    memset(abStack_38,0,0x10);
    abStack_38[0] = (byte)((ulong)lStack_20 >> 0x38);
    abStack_38[1] = (char)((ulong)lStack_20 >> 0x30);
    abStack_38[2] = (char)((ulong)lStack_20 >> 0x28);
    abStack_38[3] = (char)((ulong)lStack_20 >> 0x20);
    abStack_38[4] = (char)((ulong)lStack_20 >> 0x18);
    abStack_38[5] = (char)((ulong)lStack_20 >> 0x10);
    abStack_38[6] = (char)((ulong)lStack_20 >> 8);
    abStack_38[7] = (char)lStack_20;
    abStack_38[8] = (char)((ulong)lStack_18 >> 0x38);
    abStack_38[9] = (char)((ulong)lStack_18 >> 0x30);
    abStack_38[10] = (char)((ulong)lStack_18 >> 0x28);
    abStack_38[11] = (char)((ulong)lStack_18 >> 0x20);
    abStack_38[12] = (char)((ulong)lStack_18 >> 0x18);
    abStack_38[13] = (char)((ulong)lStack_18 >> 0x10);
    abStack_38[14] = (char)((ulong)lStack_18 >> 8);
    abStack_38[15] = (char)lStack_18;
    for (uStack_10 = 0; uStack_10 < 0x10; uStack_10 = uStack_10 + 1) {
      ctx->buf[uStack_10] = ctx->buf[uStack_10] ^ abStack_38[uStack_10];
    }
    gcm_mult(ctx,ctx->buf,ctx->buf);
    for (uStack_10 = 0; uStack_10 < tag_len; uStack_10 = uStack_10 + 1) {
      tag[uStack_10] = tag[uStack_10] ^ ctx->buf[uStack_10];
    }
  }
  return 0;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

void free(void *__ptr)

{
  free(__ptr);
  return;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

char * strncpy(char *__dest,char *__src,size_t __n)

{
  char *pcVar1;
  
  pcVar1 = strncpy(__dest,__src,__n);
  return pcVar1;
}



int gcm_start(gcm_context *ctx,int mode,uchar *iv,size_t iv_len,uchar *add,size_t add_len)

{
  ulong uStack_68;
  ulong uStack_58;
  byte abStack_38 [20];
  int iStack_24;
  ulong uStack_20;
  ulong uStack_18;
  uchar *puStack_10;
  
  memset(ctx->y,0,0x10);
  memset(ctx->buf,0,0x10);
  ctx->len = 0;
  ctx->add_len = 0;
  ctx->mode = mode;
  (ctx->aes_ctx).mode = 1;
  if (iv_len == 0xc) {
    memcpy(ctx->y,iv,0xc);
    ctx->y[0xf] = '\x01';
  }
  else {
    memset(abStack_38,0,0x10);
    abStack_38[12] = (char)((iv_len << 3) >> 0x18);
    abStack_38[13] = (char)((iv_len << 3) >> 0x10);
    abStack_38[14] = (char)((iv_len << 3) >> 8);
    abStack_38[15] = (char)((int)iv_len << 3);
    puStack_10 = iv;
    for (uStack_58 = iv_len; uStack_58 != 0; uStack_58 = uStack_58 - uStack_20) {
      uStack_20 = 0x10;
      if (uStack_58 < 0x11) {
        uStack_20 = uStack_58;
      }
      for (uStack_18 = 0; uStack_18 < uStack_20; uStack_18 = uStack_18 + 1) {
        ctx->y[uStack_18] = ctx->y[uStack_18] ^ puStack_10[uStack_18];
      }
      gcm_mult(ctx,ctx->y,ctx->y);
      puStack_10 = puStack_10 + uStack_20;
    }
    for (uStack_18 = 0; uStack_18 < 0x10; uStack_18 = uStack_18 + 1) {
      ctx->y[uStack_18] = ctx->y[uStack_18] ^ abStack_38[uStack_18];
    }
    gcm_mult(ctx,ctx->y,ctx->y);
  }
  iStack_24 = aes_cipher(&ctx->aes_ctx,ctx->y,ctx->base_ectr);
  if (iStack_24 == 0) {
    ctx->add_len = add_len;
    puStack_10 = add;
    for (uStack_68 = add_len; uStack_68 != 0; uStack_68 = uStack_68 - uStack_20) {
      uStack_20 = 0x10;
      if (uStack_68 < 0x11) {
        uStack_20 = uStack_68;
      }
      for (uStack_18 = 0; uStack_18 < uStack_20; uStack_18 = uStack_18 + 1) {
        ctx->buf[uStack_18] = ctx->buf[uStack_18] ^ puStack_10[uStack_18];
      }
      gcm_mult(ctx,ctx->buf,ctx->buf);
      puStack_10 = puStack_10 + uStack_20;
    }
    iStack_24 = 0;
  }
  return iStack_24;
}



uint8_t * datahex(char *string)

{
  char cVar1;
  uint8_t *__s;
  size_t sVar2;
  int iStack_14;
  ulong uStack_10;
  
  if (string == (char *)0x0) {
    __s = (uint8_t *)0x0;
  }
  else {
    sVar2 = strlen(string);
    if ((sVar2 & 1) == 0) {
      __s = (uint8_t *)malloc(sVar2 >> 1);
      memset(__s,0,sVar2 >> 1);
      for (uStack_10 = 0; uStack_10 < sVar2; uStack_10 = uStack_10 + 1) {
        cVar1 = string[uStack_10];
        if ((cVar1 < '0') || ('9' < cVar1)) {
          if ((cVar1 < 'A') || ('F' < cVar1)) {
            if ((cVar1 < 'a') || ('f' < cVar1)) {
              free(__s);
              return (uint8_t *)0x0;
            }
            iStack_14 = cVar1 + -0x57;
          }
          else {
            iStack_14 = cVar1 + -0x37;
          }
        }
        else {
          iStack_14 = cVar1 + -0x30;
        }
        __s[uStack_10 >> 1] =
             __s[uStack_10 >> 1] + (char)(iStack_14 << (sbyte)(((int)uStack_10 + 1U & 1) << 2));
      }
    }
    else {
      __s = (uint8_t *)0x0;
    }
  }
  return __s;
}



int gcm_crypt_and_tag(gcm_context *ctx,int mode,uchar *iv,size_t iv_len,uchar *add,size_t add_len,
                     uchar *input,uchar *output,size_t length,uchar *tag,size_t tag_len)

{
  gcm_start(ctx,mode,iv,iv_len,add,add_len);
  gcm_update(ctx,length,input,output);
  gcm_finish(ctx,tag,tag_len);
  return 0;
}



int aes_set_encryption_key(aes_context *ctx,uchar *key,uint keysize)

{
  int iVar1;
  uint *puStack_18;
  uint uStack_c;
  
  puStack_18 = ctx->rk;
  for (uStack_c = 0; uStack_c < keysize >> 2; uStack_c = uStack_c + 1) {
    puStack_18[uStack_c] =
         CONCAT13(key[uStack_c * 4 + 3],
                  CONCAT12(key[uStack_c * 4 + 2],CONCAT11(key[uStack_c * 4 + 1],key[uStack_c << 2]))
                 );
  }
  iVar1 = ctx->rounds;
  if (iVar1 == 0xe) {
    for (uStack_c = 0; uStack_c < 7; uStack_c = uStack_c + 1) {
      puStack_18[8] =
           (uint)FSb[puStack_18[7] & 0xff] << 0x18 ^
           *puStack_18 ^ RCON[uStack_c] ^ (uint)FSb[puStack_18[7] >> 8 & 0xff] ^
           (uint)FSb[puStack_18[7] >> 0x10 & 0xff] << 8 ^ (uint)FSb[puStack_18[7] >> 0x18] << 0x10;
      puStack_18[9] = puStack_18[8] ^ puStack_18[1];
      puStack_18[10] = puStack_18[9] ^ puStack_18[2];
      puStack_18[0xb] = puStack_18[10] ^ puStack_18[3];
      puStack_18[0xc] =
           (uint)FSb[puStack_18[0xb] >> 0x18] << 0x18 ^
           puStack_18[4] ^ (uint)FSb[puStack_18[0xb] & 0xff] ^
           (uint)FSb[puStack_18[0xb] >> 8 & 0xff] << 8 ^
           (uint)FSb[puStack_18[0xb] >> 0x10 & 0xff] << 0x10;
      puStack_18[0xd] = puStack_18[0xc] ^ puStack_18[5];
      puStack_18[0xe] = puStack_18[0xd] ^ puStack_18[6];
      puStack_18[0xf] = puStack_18[0xe] ^ puStack_18[7];
      puStack_18 = puStack_18 + 8;
    }
  }
  else {
    if (0xe < iVar1) {
      return -1;
    }
    if (iVar1 == 10) {
      for (uStack_c = 0; uStack_c < 10; uStack_c = uStack_c + 1) {
        puStack_18[4] =
             (uint)FSb[puStack_18[3] & 0xff] << 0x18 ^
             *puStack_18 ^ RCON[uStack_c] ^ (uint)FSb[puStack_18[3] >> 8 & 0xff] ^
             (uint)FSb[puStack_18[3] >> 0x10 & 0xff] << 8 ^ (uint)FSb[puStack_18[3] >> 0x18] << 0x10
        ;
        puStack_18[5] = puStack_18[4] ^ puStack_18[1];
        puStack_18[6] = puStack_18[5] ^ puStack_18[2];
        puStack_18[7] = puStack_18[6] ^ puStack_18[3];
        puStack_18 = puStack_18 + 4;
      }
    }
    else {
      if (iVar1 != 0xc) {
        return -1;
      }
      for (uStack_c = 0; uStack_c < 8; uStack_c = uStack_c + 1) {
        puStack_18[6] =
             (uint)FSb[puStack_18[5] & 0xff] << 0x18 ^
             *puStack_18 ^ RCON[uStack_c] ^ (uint)FSb[puStack_18[5] >> 8 & 0xff] ^
             (uint)FSb[puStack_18[5] >> 0x10 & 0xff] << 8 ^ (uint)FSb[puStack_18[5] >> 0x18] << 0x10
        ;
        puStack_18[7] = puStack_18[6] ^ puStack_18[1];
        puStack_18[8] = puStack_18[7] ^ puStack_18[2];
        puStack_18[9] = puStack_18[8] ^ puStack_18[3];
        puStack_18[10] = puStack_18[9] ^ puStack_18[4];
        puStack_18[0xb] = puStack_18[10] ^ puStack_18[5];
        puStack_18 = puStack_18 + 6;
      }
    }
  }
  return 0;
}



char * generateHexString(uchar *input,int origLen)

{
  char *__s;
  int iStack_c;
  
  __s = (char *)malloc((long)(origLen * 2 + 1));
  memset(__s,0,(long)(origLen * 2 + 1));
  for (iStack_c = 0; iStack_c < origLen; iStack_c = iStack_c + 1) {
    sprintf(__s,"%s%02X",__s,(ulong)input[iStack_c]);
  }
  return __s;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

size_t strlen(char *__s)

{
  size_t sVar1;
  
  sVar1 = strlen(__s);
  return sVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

void * memset(void *__s,int __c,size_t __n)

{
  void *pvVar1;
  
  pvVar1 = memset(__s,__c,__n);
  return pvVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

int regcomp(regex_t *__preg,char *__pattern,int __cflags)

{
  int iVar1;
  
  iVar1 = regcomp(__preg,__pattern,__cflags);
  return iVar1;
}



char * extractValues(char *key,char *req)

{
  size_t sVar1;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined4 uStack_38;
  char *pcStack_28;
  char *pcStack_20;
  char *pcStack_18;
  char *pcStack_10;
  
  uStack_98 = 0;
  uStack_90 = 0;
  uStack_88 = 0;
  uStack_80 = 0;
  uStack_78 = 0;
  uStack_70 = 0;
  uStack_68 = 0;
  uStack_60 = 0;
  uStack_58 = 0;
  uStack_50 = 0;
  uStack_48 = 0;
  uStack_40 = 0;
  uStack_38 = 0;
  pcStack_10 = (char *)0x0;
  pcStack_18 = (char *)0x0;
  pcStack_20 = strdup(req);
  sVar1 = strlen(key);
  if (sVar1 < 0x15) {
    sprintf((char *)&uStack_98,"<%s val=\"",key);
    pcStack_10 = strstr(pcStack_20,(char *)&uStack_98);
    if (pcStack_10 != (char *)0x0) {
      sVar1 = strlen((char *)&uStack_98);
      pcStack_10 = pcStack_10 + sVar1;
      pcStack_18 = strtok(pcStack_10,"\"");
      if (pcStack_18 != (char *)0x0) {
        sVar1 = strlen(pcStack_18);
        pcStack_28 = (char *)malloc(sVar1 + 1);
        sVar1 = strlen(pcStack_18);
        memset(pcStack_28,0,sVar1 + 1);
        sVar1 = strlen(pcStack_18);
        strncpy(pcStack_28,pcStack_18,sVar1);
        free(pcStack_20);
        return pcStack_28;
      }
    }
    fwrite("ERROR\n",1,6,stderr);
    free(pcStack_20);
  }
  return (char *)0x0;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

void srand(uint __seed)

{
  srand(__seed);
  return;
}



int gcm_update(gcm_context *ctx,size_t length,uchar *input,uchar *output)

{
  uchar *puStack_58;
  uchar *puStack_50;
  ulong uStack_48;
  byte abStack_38 [28];
  int iStack_1c;
  ulong uStack_18;
  ulong uStack_10;
  
  ctx->len = ctx->len + length;
  puStack_58 = output;
  puStack_50 = input;
  uStack_48 = length;
  while( true ) {
    if (uStack_48 == 0) {
      return 0;
    }
    uStack_18 = 0x10;
    if (uStack_48 < 0x11) {
      uStack_18 = uStack_48;
    }
    for (uStack_10 = 0x10;
        (0xc < uStack_10 &&
        (ctx->base_ectr[uStack_10 + 0xf] = ctx->base_ectr[uStack_10 + 0xf] + '\x01',
        ctx->base_ectr[uStack_10 + 0xf] == '\0')); uStack_10 = uStack_10 - 1) {
    }
    iStack_1c = aes_cipher(&ctx->aes_ctx,ctx->y,abStack_38);
    if (iStack_1c != 0) break;
    if (ctx->mode == 1) {
      for (uStack_10 = 0; uStack_10 < uStack_18; uStack_10 = uStack_10 + 1) {
        puStack_58[uStack_10] = abStack_38[uStack_10] ^ puStack_50[uStack_10];
        ctx->buf[uStack_10] = ctx->buf[uStack_10] ^ puStack_58[uStack_10];
      }
    }
    else {
      for (uStack_10 = 0; uStack_10 < uStack_18; uStack_10 = uStack_10 + 1) {
        ctx->buf[uStack_10] = ctx->buf[uStack_10] ^ puStack_50[uStack_10];
        puStack_58[uStack_10] = abStack_38[uStack_10] ^ puStack_50[uStack_10];
      }
    }
    gcm_mult(ctx,ctx->buf,ctx->buf);
    uStack_48 = uStack_48 - uStack_18;
    puStack_50 = puStack_50 + uStack_18;
    puStack_58 = puStack_58 + uStack_18;
  }
  return iStack_1c;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

void * memcpy(void *__dest,void *__src,size_t __n)

{
  void *pvVar1;
  
  pvVar1 = memcpy(__dest,__src,__n);
  return pvVar1;
}



int aes_setkey(aes_context *ctx,int mode,uchar *key,uint keysize)

{
  int iVar1;
  
  if (aes_tables_inited == 0) {
    return -1;
  }
  ctx->mode = mode;
  ctx->rk = ctx->buf;
  if (keysize == 0x20) {
    ctx->rounds = 0xe;
  }
  else {
    if (0x20 < keysize) {
      return -1;
    }
    if (keysize == 0x10) {
      ctx->rounds = 10;
    }
    else {
      if (keysize != 0x18) {
        return -1;
      }
      ctx->rounds = 0xc;
    }
  }
  iVar1 = aes_set_encryption_key(ctx,key,keysize);
  return iVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

time_t time(time_t *__timer)

{
  time_t tVar1;
  
  tVar1 = time(__timer);
  return tVar1;
}



int gcm_auth_decrypt(gcm_context *ctx,uchar *iv,size_t iv_len,uchar *add,size_t add_len,uchar *input
                    ,uchar *output,size_t length,uchar *tag,size_t tag_len)

{
  int iVar1;
  byte abStack_28 [16];
  ulong uStack_18;
  uint uStack_c;
  
  gcm_crypt_and_tag(ctx,0,iv,iv_len,add,add_len,input,output,length,abStack_28,tag_len);
  uStack_c = 0;
  for (uStack_18 = 0; uStack_18 < tag_len; uStack_18 = uStack_18 + 1) {
    uStack_c = uStack_c | abStack_28[uStack_18] ^ tag[uStack_18];
  }
  if (uStack_c == 0) {
    iVar1 = 0;
  }
  else {
    memset(output,0,length);
    iVar1 = 0x55555555;
  }
  return iVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

void * malloc(size_t __size)

{
  void *pvVar1;
  
  pvVar1 = malloc(__size);
  return pvVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

int regexec(regex_t *__preg,char *__string,size_t __nmatch,regmatch_t *__pmatch,int __eflags)

{
  int iVar1;
  
  iVar1 = regexec(__preg,__string,__nmatch,__pmatch,__eflags);
  return iVar1;
}



void build_decoding_table(void)

{
  int iStack_c;
  
  decoding_table = (char *)malloc(0x100);
  for (iStack_c = 0; iStack_c < 0x40; iStack_c = iStack_c + 1) {
    decoding_table
    [(byte)"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[iStack_c]] =
         (char)iStack_c;
  }
  return;
}



int gcm_setkey(gcm_context *ctx,uchar *key,uint keysize)

{
  ulong uVar1;
  ulong uVar2;
  uint uVar3;
  byte bStack_68;
  byte bStack_67;
  byte bStack_66;
  byte bStack_65;
  byte bStack_64;
  byte bStack_63;
  byte bStack_62;
  byte bStack_61;
  byte bStack_60;
  byte bStack_5f;
  byte bStack_5e;
  byte bStack_5d;
  byte bStack_5c;
  byte bStack_5b;
  byte bStack_5a;
  byte bStack_59;
  int iStack_24;
  uint64_t uStack_20;
  uint64_t uStack_18;
  int iStack_10;
  int iStack_c;
  
  memset(ctx,0,0x268);
  memset(&bStack_68,0,0x10);
  iStack_24 = aes_setkey(&ctx->aes_ctx,1,key,keysize);
  if ((iStack_24 == 0) &&
     (iStack_24 = aes_cipher(&ctx->aes_ctx,&bStack_68,&bStack_68), iStack_24 == 0)) {
    uStack_20 = CONCAT44((uint)bStack_65 |
                         (uint)bStack_68 << 0x18 | (uint)bStack_67 << 0x10 | (uint)bStack_66 << 8,
                         (uint)bStack_61 |
                         (uint)bStack_64 << 0x18 | (uint)bStack_63 << 0x10 | (uint)bStack_62 << 8);
    uStack_18 = CONCAT44((uint)bStack_5d |
                         (uint)bStack_60 << 0x18 | (uint)bStack_5f << 0x10 | (uint)bStack_5e << 8,
                         (uint)bStack_59 |
                         (uint)bStack_5c << 0x18 | (uint)bStack_5b << 0x10 | (uint)bStack_5a << 8);
    ctx->HL[8] = uStack_18;
    ctx->HH[8] = uStack_20;
    ctx->HH[0] = 0;
    ctx->HL[0] = 0;
    for (iStack_c = 4; iStack_c != 0; iStack_c = iStack_c >> 1) {
      uVar3 = (uint)uStack_18;
      uStack_18 = uStack_18 >> 1 | uStack_20 << 0x3f;
      uStack_20 = (ulong)((uVar3 & 1) * -0x1f000000) << 0x20 ^ uStack_20 >> 1;
      ctx->HL[iStack_c] = uStack_18;
      ctx->HH[iStack_c] = uStack_20;
    }
    for (iStack_c = 2; iStack_c < 0x10; iStack_c = iStack_c << 1) {
      uVar1 = ctx->HH[iStack_c];
      uVar2 = ctx->HL[iStack_c];
      for (iStack_10 = 1; iStack_10 < iStack_c; iStack_10 = iStack_10 + 1) {
        (ctx->HH + iStack_c)[iStack_10] = ctx->HH[iStack_10] ^ uVar1;
        (ctx->HL + iStack_c)[iStack_10] = ctx->HL[iStack_10] ^ uVar2;
      }
    }
    iStack_24 = 0;
  }
  return iStack_24;
}



void aes_init_keygen_tables(void)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  int aiStack_818 [256];
  uint auStack_418 [257];
  uint uStack_14;
  uint uStack_10;
  int iStack_c;
  
  if (aes_tables_inited == 0) {
    uStack_10 = 1;
    for (iStack_c = 0; iStack_c < 0x100; iStack_c = iStack_c + 1) {
      auStack_418[iStack_c] = uStack_10;
      aiStack_818[(int)uStack_10] = iStack_c;
      if ((uStack_10 & 0x80) == 0) {
        uVar3 = 0;
      }
      else {
        uVar3 = 0x1b;
      }
      uStack_10 = (uVar3 ^ uStack_10 * 2 ^ uStack_10) & 0xff;
    }
    uStack_10 = 1;
    for (iStack_c = 0; iStack_c < 10; iStack_c = iStack_c + 1) {
      RCON[iStack_c] = uStack_10;
      if ((uStack_10 & 0x80) == 0) {
        uVar3 = 0;
      }
      else {
        uVar3 = 0x1b;
      }
      uStack_10 = (uVar3 ^ uStack_10 * 2) & 0xff;
    }
    FSb[0] = 'c';
    for (iStack_c = 1; iStack_c < 0x100; iStack_c = iStack_c + 1) {
      uVar3 = auStack_418[0xff - aiStack_818[iStack_c]];
      uVar4 = ((int)uVar3 >> 7 | uVar3 * 2) & 0xff;
      uVar1 = (int)uVar4 >> 7 | uVar4 * 2 & 0xff;
      uVar2 = (int)uVar1 >> 7 | uVar1 * 2 & 0xff;
      uStack_14 = (int)uVar2 >> 7 | uVar2 * 2 & 0xff;
      uStack_10 = uVar3 ^ uVar4 ^ uVar1 ^ uVar2 ^ uStack_14 ^ 99;
      FSb[iStack_c] = (uchar)uStack_10;
    }
    for (iStack_c = 0; iStack_c < 0x100; iStack_c = iStack_c + 1) {
      uVar3 = (uint)FSb[iStack_c];
      if ((FSb[iStack_c] & 0x80) == 0) {
        uVar4 = 0;
      }
      else {
        uVar4 = 0x1b;
      }
      uVar4 = (uVar4 ^ uVar3 * 2) & 0xff;
      FT0[iStack_c] = uVar3 << 8 ^ uVar4 ^ uVar3 << 0x10 ^ (uVar4 ^ uVar3) << 0x18;
      FT1[iStack_c] = FT0[iStack_c] << 8 | FT0[iStack_c] >> 0x18;
      FT2[iStack_c] = FT1[iStack_c] << 8 | FT1[iStack_c] >> 0x18;
      FT3[iStack_c] = FT2[iStack_c] << 8 | FT2[iStack_c] >> 0x18;
    }
    aes_tables_inited = 1;
  }
  return;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

char * strtok(char *__s,char *__delim)

{
  char *pcVar1;
  
  pcVar1 = strtok(__s,__delim);
  return pcVar1;
}



int aes_cipher(aes_context *ctx,uchar *input,uchar *output)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  byte bVar10;
  byte bVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  byte bVar15;
  uint *puVar16;
  uint uVar17;
  uint uVar18;
  uint uVar19;
  uint uVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  uint uStack_28;
  uint uStack_24;
  uint uStack_20;
  uint uStack_1c;
  uint *puStack_18;
  int iStack_c;
  
  puVar16 = ctx->rk;
  uStack_1c = *(uint *)input ^ *puVar16;
  uStack_20 = *(uint *)(input + 4) ^ puVar16[1];
  uStack_24 = *(uint *)(input + 8) ^ puVar16[2];
  puStack_18 = puVar16 + 4;
  uStack_28 = *(uint *)(input + 0xc) ^ puVar16[3];
  iStack_c = ctx->rounds >> 1;
  while (iStack_c = iStack_c + -1, 0 < iStack_c) {
    uVar17 = FT3[uStack_28 >> 0x18] ^
             *puStack_18 ^ FT0[uStack_1c & 0xff] ^ FT1[uStack_20 >> 8 & 0xff] ^
             FT2[uStack_24 >> 0x10 & 0xff];
    uVar18 = FT3[uStack_1c >> 0x18] ^
             puStack_18[1] ^ FT0[uStack_20 & 0xff] ^ FT1[uStack_24 >> 8 & 0xff] ^
             FT2[uStack_28 >> 0x10 & 0xff];
    uVar19 = FT3[uStack_20 >> 0x18] ^
             puStack_18[2] ^ FT0[uStack_24 & 0xff] ^ FT1[uStack_28 >> 8 & 0xff] ^
             FT2[uStack_1c >> 0x10 & 0xff];
    uVar20 = FT3[uStack_24 >> 0x18] ^
             puStack_18[3] ^ FT0[uStack_28 & 0xff] ^ FT1[uStack_1c >> 8 & 0xff] ^
             FT2[uStack_20 >> 0x10 & 0xff];
    uStack_1c = FT3[uVar20 >> 0x18] ^
                puStack_18[4] ^ FT0[uVar17 & 0xff] ^ FT1[uVar18 >> 8 & 0xff] ^
                FT2[uVar19 >> 0x10 & 0xff];
    uStack_20 = FT3[uVar17 >> 0x18] ^
                puStack_18[5] ^ FT0[uVar18 & 0xff] ^ FT1[uVar19 >> 8 & 0xff] ^
                FT2[uVar20 >> 0x10 & 0xff];
    puVar16 = puStack_18 + 7;
    uStack_24 = FT3[uVar18 >> 0x18] ^
                puStack_18[6] ^ FT0[uVar19 & 0xff] ^ FT1[uVar20 >> 8 & 0xff] ^
                FT2[uVar17 >> 0x10 & 0xff];
    puStack_18 = puStack_18 + 8;
    uStack_28 = FT3[uVar19 >> 0x18] ^
                *puVar16 ^ FT0[uVar20 & 0xff] ^ FT1[uVar17 >> 8 & 0xff] ^ FT2[uVar18 >> 0x10 & 0xff]
    ;
  }
  uVar21 = FT3[uStack_28 >> 0x18] ^
           *puStack_18 ^ FT0[uStack_1c & 0xff] ^ FT1[uStack_20 >> 8 & 0xff] ^
           FT2[uStack_24 >> 0x10 & 0xff];
  uVar22 = FT3[uStack_1c >> 0x18] ^
           puStack_18[1] ^ FT0[uStack_20 & 0xff] ^ FT1[uStack_24 >> 8 & 0xff] ^
           FT2[uStack_28 >> 0x10 & 0xff];
  uVar23 = FT3[uStack_20 >> 0x18] ^
           puStack_18[2] ^ FT0[uStack_24 & 0xff] ^ FT1[uStack_28 >> 8 & 0xff] ^
           FT2[uStack_1c >> 0x10 & 0xff];
  uVar24 = FT3[uStack_24 >> 0x18] ^
           puStack_18[3] ^ FT0[uStack_28 & 0xff] ^ FT1[uStack_1c >> 8 & 0xff] ^
           FT2[uStack_20 >> 0x10 & 0xff];
  uVar17 = puStack_18[4];
  bVar1 = FSb[uVar22 >> 8 & 0xff];
  bVar2 = FSb[uVar23 >> 0x10 & 0xff];
  bVar3 = FSb[uVar24 >> 0x18];
  uVar18 = puStack_18[5];
  bVar4 = FSb[uVar22 & 0xff];
  bVar5 = FSb[uVar23 >> 8 & 0xff];
  bVar6 = FSb[uVar24 >> 0x10 & 0xff];
  bVar7 = FSb[uVar21 >> 0x18];
  uVar19 = puStack_18[6];
  bVar8 = FSb[uVar23 & 0xff];
  bVar9 = FSb[uVar24 >> 8 & 0xff];
  bVar10 = FSb[uVar21 >> 0x10 & 0xff];
  bVar11 = FSb[uVar22 >> 0x18];
  uVar20 = puStack_18[7];
  bVar12 = FSb[uVar24 & 0xff];
  bVar13 = FSb[uVar21 >> 8 & 0xff];
  bVar14 = FSb[uVar22 >> 0x10 & 0xff];
  bVar15 = FSb[uVar23 >> 0x18];
  *output = (byte)uVar17 ^ FSb[uVar21 & 0xff];
  output[1] = (byte)(uVar17 >> 8) ^ bVar1;
  output[2] = (byte)(uVar17 >> 0x10) ^ bVar2;
  output[3] = bVar3 ^ (byte)(uVar17 >> 0x18);
  output[4] = (byte)uVar18 ^ bVar4;
  output[5] = (byte)(uVar18 >> 8) ^ bVar5;
  output[6] = (byte)(uVar18 >> 0x10) ^ bVar6;
  output[7] = bVar7 ^ (byte)(uVar18 >> 0x18);
  output[8] = (byte)uVar19 ^ bVar8;
  output[9] = (byte)(uVar19 >> 8) ^ bVar9;
  output[10] = (byte)(uVar19 >> 0x10) ^ bVar10;
  output[0xb] = bVar11 ^ (byte)(uVar19 >> 0x18);
  output[0xc] = (byte)uVar20 ^ bVar12;
  output[0xd] = (byte)(uVar20 >> 8) ^ bVar13;
  output[0xe] = (byte)(uVar20 >> 0x10) ^ bVar14;
  output[0xf] = bVar15 ^ (byte)(uVar20 >> 0x18);
  return 0;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

int sprintf(char *__s,char *__format,...)

{
  int iVar1;
  
  iVar1 = sprintf(__s,__format);
  return iVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

size_t fwrite(void *__ptr,size_t __size,size_t __n,FILE *__s)

{
  size_t sVar1;
  
  sVar1 = fwrite(__ptr,__size,__n,__s);
  return sVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

char * strdup(char *__s)

{
  char *pcVar1;
  
  pcVar1 = strdup(__s);
  return pcVar1;
}



int gcm_initialize(void)

{
  aes_init_keygen_tables();
  return 0;
}



void generateNonce(char *data)

{
  int iVar1;
  time_t tVar2;
  int iStack_c;
  
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  for (iStack_c = 0; iStack_c < 0xc; iStack_c = iStack_c + 1) {
    iVar1 = rand();
    data[iStack_c] = (char)iVar1;
  }
  return;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

char * strstr(char *__haystack,char *__needle)

{
  char *pcVar1;
  
  pcVar1 = strstr(__haystack,__needle);
  return pcVar1;
}



// WARNING: Unknown calling convention -- yet parameter storage is locked

int rand(void)

{
  int iVar1;
  
  iVar1 = rand();
  return iVar1;
}



// WARNING: Removing unreachable block (ram,0x00102473)
// WARNING: Removing unreachable block (ram,0x0010247f)

void deregister_tm_clones(void)

{
  return;
}



// WARNING: Removing unreachable block (ram,0x001024b4)
// WARNING: Removing unreachable block (ram,0x001024c0)

void register_tm_clones(void)

{
  return;
}



void __do_global_dtors_aux(void)

{
  if (completed_8061 != '\0') {
    return;
  }
  __cxa_finalize(&__dso_handle);
  deregister_tm_clones();
  completed_8061 = 1;
  return;
}



void frame_dummy(void)

{
  register_tm_clones();
  return;
}



uint8_t * datahex(char *string)

{
  char cVar1;
  uint8_t *__s;
  size_t sVar2;
  char c;
  uint8_t *data;
  size_t dlength;
  size_t slength;
  int value;
  size_t index;
  
  if (string == (char *)0x0) {
    __s = (uint8_t *)0x0;
  }
  else {
    sVar2 = strlen(string);
    if ((sVar2 & 1) == 0) {
      __s = (uint8_t *)malloc(sVar2 >> 1);
      memset(__s,0,sVar2 >> 1);
      for (index = 0; index < sVar2; index = index + 1) {
        cVar1 = string[index];
        if ((cVar1 < '0') || ('9' < cVar1)) {
          if ((cVar1 < 'A') || ('F' < cVar1)) {
            if ((cVar1 < 'a') || ('f' < cVar1)) {
              free(__s);
              return (uint8_t *)0x0;
            }
            value = cVar1 + -0x57;
          }
          else {
            value = cVar1 + -0x37;
          }
        }
        else {
          value = cVar1 + -0x30;
        }
        __s[index >> 1] = __s[index >> 1] + (char)(value << (sbyte)(((int)index + 1U & 1) << 2));
      }
    }
    else {
      __s = (uint8_t *)0x0;
    }
  }
  return __s;
}



void decrypt_request(char *ciphertext,char *iv,size_t ciphertext_len,char **plaintext)

{
  return;
}



int validate_request(char *request)

{
  int iVar1;
  char regexPattern [50];
  regex_t regex;
  uint8_t subkey_match [5];
  char *subkeys [5];
  int ret;
  char *root;
  
  regexPattern._0_8_ = 0;
  regexPattern._8_8_ = 0;
  regexPattern._16_8_ = 0;
  regexPattern._24_8_ = 0;
  regexPattern._32_8_ = 0;
  regexPattern._40_8_ = 0;
  regexPattern._48_2_ = 0;
  sprintf(regexPattern,"<%s>[\\s\\S]*?<\\/%s>",&DAT_00106040,&DAT_00106040);
  iVar1 = regcomp((regex_t *)&regex,request,0);
  if (iVar1 == 0) {
    iVar1 = regexec((regex_t *)&regex,request,0,(regmatch_t *)0x0,0);
    if (iVar1 == 0) {
      iVar1 = 0;
    }
    else {
      iVar1 = 1;
    }
  }
  else {
    iVar1 = 1;
  }
  return iVar1;
}



char * extractValues(char *key,char *req)

{
  char *__haystack;
  size_t sVar1;
  char *pcVar2;
  char *__dest;
  char searchstring [100];
  char *ret;
  char *request;
  char *copier;
  char *token;
  
  searchstring._0_8_ = 0;
  searchstring._8_8_ = 0;
  searchstring._16_8_ = 0;
  searchstring._24_8_ = 0;
  searchstring._32_8_ = 0;
  searchstring._40_8_ = 0;
  searchstring._48_8_ = 0;
  searchstring._56_8_ = 0;
  searchstring._64_8_ = 0;
  searchstring._72_8_ = 0;
  searchstring._80_8_ = 0;
  searchstring._88_8_ = 0;
  searchstring._96_4_ = 0;
  __haystack = strdup(req);
  sVar1 = strlen(key);
  if (sVar1 < 0x15) {
    sprintf(searchstring,"<%s val=\"",key);
    pcVar2 = strstr(__haystack,searchstring);
    if (pcVar2 != (char *)0x0) {
      sVar1 = strlen(searchstring);
      pcVar2 = strtok(pcVar2 + sVar1,"\"");
      if (pcVar2 != (char *)0x0) {
        sVar1 = strlen(pcVar2);
        __dest = (char *)malloc(sVar1 + 1);
        sVar1 = strlen(pcVar2);
        memset(__dest,0,sVar1 + 1);
        sVar1 = strlen(pcVar2);
        strncpy(__dest,pcVar2,sVar1);
        free(__haystack);
        return __dest;
      }
    }
    fwrite("ERROR\n",1,6,stderr);
    free(__haystack);
  }
  return (char *)0x0;
}



void generateNonce(char *data)

{
  int iVar1;
  time_t tVar2;
  int i;
  
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  for (i = 0; i < 0xc; i = i + 1) {
    iVar1 = rand();
    data[i] = (char)iVar1;
  }
  return;
}



char * generateHexString(uchar *input,int origLen)

{
  char *__s;
  char *ret;
  int i;
  
  __s = (char *)malloc((long)(origLen * 2 + 1));
  memset(__s,0,(long)(origLen * 2 + 1));
  for (i = 0; i < origLen; i = i + 1) {
    sprintf(__s,"%s%02X",__s,(ulong)input[i]);
  }
  return __s;
}



char * stringParser(char *rawDataBody,uint32_t payload_size)

{
  int ctx_len_half;
  uchar *output;
  uchar *tag;
  uchar *output_00;
  char *__s;
  char *pcVar1;
  uint8_t *iv;
  size_t enc_passwd_len;
  uint8_t *auth_tag;
  size_t action_len;
  uint8_t *enc_data;
  char *pcVar2;
  char *pcVar3;
  long lVar4;
  undefined8 *puVar5;
  char *redeemer [4];
  gcm_context ctx2;
  gcm_context key;
  uint8_t redeemselector;
  uchar return_nonce_data [12];
  char M_response_cleartext [256];
  char received_aead [33];
  char received_ctx [1025];
  char received_nonce [25];
  char *TODO;
  char *adminVerifyer;
  char *combinedResponse;
  char *return_aead;
  char *return_ctx;
  char *return_nonce;
  int return_aead_data_len;
  int return_ctx_data_len;
  int return_nonce_data_len;
  uchar *return_ctx_data;
  uchar *return_aead_data;
  char *action;
  char *enc_paswd;
  char *received_plaintext;
  int received_aead_data_len;
  int received_ctx_data_len;
  int received_nonce_data_len;
  uchar *received_aead_data;
  uchar *received_ctx_data;
  uchar *received_nonce_data;
  int ret;
  
  received_nonce._0_8_ = 0;
  received_nonce._8_8_ = 0;
  received_nonce._16_8_ = 0;
  received_nonce[24] = '\0';
  received_ctx._0_8_ = 0;
  received_ctx._8_8_ = 0;
  puVar5 = (undefined8 *)(received_ctx + 0x10);
  for (lVar4 = 0x7e; lVar4 != 0; lVar4 = lVar4 + -1) {
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  *(undefined *)puVar5 = 0;
  received_aead._0_8_ = 0;
  received_aead._8_8_ = 0;
  received_aead._16_8_ = 0;
  received_aead._24_8_ = 0;
  received_aead[32] = '\0';
  output = (uchar *)malloc(1000);
  memset(output,0,1000);
  M_response_cleartext._0_8_ = 0;
  M_response_cleartext._8_8_ = 0;
  M_response_cleartext._16_8_ = 0;
  M_response_cleartext._24_8_ = 0;
  M_response_cleartext._32_8_ = 0;
  M_response_cleartext._40_8_ = 0;
  M_response_cleartext._48_8_ = 0;
  M_response_cleartext._56_8_ = 0;
  M_response_cleartext._64_8_ = 0;
  M_response_cleartext._72_8_ = 0;
  M_response_cleartext._80_8_ = 0;
  M_response_cleartext._88_8_ = 0;
  M_response_cleartext._96_8_ = 0;
  M_response_cleartext._104_8_ = 0;
  M_response_cleartext._112_8_ = 0;
  M_response_cleartext._120_8_ = 0;
  M_response_cleartext._128_8_ = 0;
  M_response_cleartext._136_8_ = 0;
  M_response_cleartext._144_8_ = 0;
  M_response_cleartext._152_8_ = 0;
  M_response_cleartext._160_8_ = 0;
  M_response_cleartext._168_8_ = 0;
  M_response_cleartext._176_8_ = 0;
  M_response_cleartext._184_8_ = 0;
  M_response_cleartext._192_8_ = 0;
  M_response_cleartext._200_8_ = 0;
  M_response_cleartext._208_8_ = 0;
  M_response_cleartext._216_8_ = 0;
  M_response_cleartext._224_8_ = 0;
  M_response_cleartext._232_8_ = 0;
  M_response_cleartext._240_8_ = 0;
  M_response_cleartext._248_8_ = 0;
  tag = (uchar *)malloc(0x10);
  output_00 = (uchar *)malloc(0x200);
  memset(output_00,0,0x200);
  __s = (char *)malloc(0x500);
  memset(__s,0,0x500);
  pcVar1 = strstr(rawDataBody,"SYN?");
  if (pcVar1 == (char *)0x0) {
    fwrite("Received Request from Manager\n",1,0x1e,stderr);
    if (payload_size == 0x238) {
      memcpy(received_nonce,rawDataBody,0x18);
      enc_passwd_len = strlen(received_nonce);
      if (enc_passwd_len == 0x18) {
        memcpy(received_ctx,rawDataBody + 0x18,0x200);
        memcpy(received_aead,rawDataBody + 0x218,0x20);
        redeemselector = 0xff;
        if ((dword *)&stack0x00000000 == &DWORD_001065e0) {
          redeemselector = '\0';
          verifyer_second = '\0';
        }
        iv = datahex(received_nonce);
        enc_passwd_len = strlen(received_nonce);
        auth_tag = datahex(received_ctx);
        action_len = strlen(received_ctx);
        ctx_len_half = (int)(action_len >> 1);
        if (ctx_len_half < 0x321) {
          enc_data = datahex(received_aead);
          action_len = strlen(received_aead);
          gcm_initialize();
          gcm_setkey(&key,key_M_SP,0x20);
          ctx_len_half = gcm_auth_decrypt(&key,iv,(long)(int)(enc_passwd_len >> 1),(uchar *)0x0,0,
                                          auth_tag,output,(long)ctx_len_half,enc_data,
                                          (long)(int)(action_len >> 1));
          if (ctx_len_half == 0) {
            pcVar1 = extractValues("enc_paswd",(char *)output);
            if (pcVar1 == (char *)0x0) {
              __s = "ERROR WHILE HANDLING REQUEST";
            }
            else {
              pcVar2 = extractValues("action",(char *)output);
              if (pcVar2 == (char *)0x0) {
                __s = "ERROR WHILE HANDLING REQUEST";
              }
              else {
                enc_passwd_len = strlen(pcVar1);
                action_len = strlen(pcVar2);
                if (action_len + enc_passwd_len < 100) {
                  sprintf(M_response_cleartext,"%s,%s",pcVar1,pcVar2);
                  generateNonce((char *)return_nonce_data);
                  gcm_initialize();
                  gcm_setkey(&ctx2,key_M_SP,0x20);
                  if (redirectAdmin == 0x7d316c) {
                    redeemer[0] = "d3c0y";
                    redeemer[1] = "f4k3";
                    redeemer[2] = "doublef4k3";
                    redeemer[3] = "token";
                    pcVar1 = extractValues(redeemer[(int)(uint)redeemselector],(char *)output);
                    if ((verifyer_second == '\x14') || (pcVar1 == (char *)0x0)) {
                      return "ERROR WHILE HANDLING REQUEST";
                    }
                    memset(M_response_cleartext,0,0x100);
                    sprintf(M_response_cleartext,"redeemToken,%s",pcVar1);
                  }
                  gcm_crypt_and_tag(&ctx2,1,return_nonce_data,0xc,(uchar *)0x0,0,
                                    (uchar *)M_response_cleartext,output_00,0x100,tag,0x10);
                  pcVar1 = generateHexString(return_nonce_data,0xc);
                  pcVar2 = generateHexString(output_00,0x100);
                  pcVar3 = generateHexString(tag,0x10);
                  sprintf(__s,"%s%s%s",pcVar1,pcVar2,pcVar3);
                  fwrite("Sending Response to Manager\n",1,0x1c,stderr);
                }
                else {
                  __s = "ERROR WHILE HANDLING REQUEST";
                }
              }
            }
          }
          else {
            __s = "ERROR WHILE HANDLING REQUEST";
          }
        }
        else {
          __s = "ERROR WHILE HANDLING REQUEST";
        }
      }
      else {
        __s = "ERROR WHILE HANDLING REQUEST";
      }
    }
    else {
      __s = "ERROR WHILE HANDLING REQUEST";
    }
  }
  else {
    __s = "ACK!";
  }
  return __s;
}



char * base64_encode(uchar *data,size_t input_length,size_t *output_length)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  char *pcVar5;
  uint32_t triple;
  uint32_t octet_c;
  uint32_t octet_b;
  uint32_t octet_a;
  char *encoded_data;
  int i_1;
  int j;
  int i;
  
  *output_length = ((input_length + 2) / 3) * 4;
  pcVar5 = (char *)malloc(*output_length);
  if (pcVar5 == (char *)0x0) {
    pcVar5 = (char *)0x0;
  }
  else {
    i = 0;
    j = 0;
    while ((ulong)(long)i < input_length) {
      if ((ulong)(long)i < input_length) {
        uVar2 = (uint)data[i];
        i = i + 1;
      }
      else {
        uVar2 = 0;
      }
      if ((ulong)(long)i < input_length) {
        uVar3 = (uint)data[i];
        i = i + 1;
      }
      else {
        uVar3 = 0;
      }
      if ((ulong)(long)i < input_length) {
        uVar4 = (uint)data[i];
        i = i + 1;
      }
      else {
        uVar4 = 0;
      }
      uVar4 = uVar4 + uVar2 * 0x10000 + uVar3 * 0x100;
      pcVar5[j] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
                  [uVar4 >> 0x12 & 0x3f];
      pcVar5[j + 1] =
           "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[uVar4 >> 0xc & 0x3f];
      iVar1 = j + 3;
      pcVar5[j + 2] =
           "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[uVar4 >> 6 & 0x3f];
      j = j + 4;
      pcVar5[iVar1] =
           "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[uVar4 & 0x3f];
    }
    for (i_1 = 0; i_1 < mod_table[input_length % 3]; i_1 = i_1 + 1) {
      pcVar5[(*output_length - (long)i_1) + -1] = '=';
    }
  }
  return pcVar5;
}



uchar * base64_decode(char *data,size_t input_length,size_t *output_length)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uchar *puVar6;
  uint32_t triple;
  uint32_t sextet_d;
  uint32_t sextet_c;
  uint32_t sextet_b;
  uint32_t sextet_a;
  uchar *decoded_data;
  int j;
  int i;
  
  if (decoding_table == (char *)0x0) {
    build_decoding_table();
  }
  if ((input_length & 3) == 0) {
    *output_length = (input_length >> 2) * 3;
    if (data[input_length - 1] == '=') {
      *output_length = *output_length - 1;
    }
    if (data[input_length - 2] == '=') {
      *output_length = *output_length - 1;
    }
    puVar6 = (uchar *)malloc(*output_length);
    if (puVar6 == (uchar *)0x0) {
      puVar6 = (uchar *)0x0;
    }
    else {
      i = 0;
      j = 0;
      while (iVar1 = i, (ulong)(long)i < input_length) {
        if (data[i] == '=') {
          iVar2 = 0;
        }
        else {
          iVar2 = (int)decoding_table[data[i]];
        }
        i = i + 1;
        if (data[i] == '=') {
          iVar3 = 0;
        }
        else {
          iVar3 = (int)decoding_table[data[i]];
        }
        i = iVar1 + 2;
        if (data[i] == '=') {
          iVar4 = 0;
        }
        else {
          iVar4 = (int)decoding_table[data[i]];
        }
        i = iVar1 + 3;
        if (data[i] == '=') {
          iVar5 = 0;
        }
        else {
          iVar5 = (int)decoding_table[data[i]];
        }
        i = iVar1 + 4;
        iVar5 = iVar5 + iVar2 * 0x40000 + iVar3 * 0x1000 + iVar4 * 0x40;
        if ((ulong)(long)j < *output_length) {
          puVar6[j] = (uchar)((uint)iVar5 >> 0x10);
          j = j + 1;
        }
        if ((ulong)(long)j < *output_length) {
          puVar6[j] = (uchar)((uint)iVar5 >> 8);
          j = j + 1;
        }
        if ((ulong)(long)j < *output_length) {
          puVar6[j] = (uchar)iVar5;
          j = j + 1;
        }
      }
    }
  }
  else {
    puVar6 = (uchar *)0x0;
  }
  return puVar6;
}



void build_decoding_table(void)

{
  int i;
  
  decoding_table = (char *)malloc(0x100);
  for (i = 0; i < 0x40; i = i + 1) {
    decoding_table[(byte)"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[i]] =
         (char)i;
  }
  return;
}



void base64_cleanup(void)

{
  free(decoding_table);
  return;
}



void aes_init_keygen_tables(void)

{
  int iVar1;
  byte bVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  int log [256];
  int pow [256];
  int z;
  int y;
  int x;
  int i;
  
  if (aes_tables_inited == 0) {
    x = 1;
    for (i = 0; i < 0x100; i = i + 1) {
      pow[i] = x;
      log[x] = i;
      if ((x & 0x80U) == 0) {
        uVar3 = 0;
      }
      else {
        uVar3 = 0x1b;
      }
      x = (uVar3 ^ x * 2 ^ x) & 0xff;
    }
    x = 1;
    for (i = 0; i < 10; i = i + 1) {
      RCON[i] = x;
      if ((x & 0x80U) == 0) {
        uVar3 = 0;
      }
      else {
        uVar3 = 0x1b;
      }
      x = (uVar3 ^ x * 2) & 0xff;
    }
    FSb[0] = 'c';
    for (i = 1; i < 0x100; i = i + 1) {
      iVar1 = pow[0xff - log[i]];
      uVar3 = (iVar1 >> 7 | iVar1 * 2) & 0xff;
      uVar5 = (int)uVar3 >> 7 | uVar3 * 2 & 0xff;
      uVar4 = (int)uVar5 >> 7 | uVar5 * 2 & 0xff;
      bVar2 = (byte)uVar4;
      FSb[i] = (byte)iVar1 ^ (byte)uVar3 ^ (byte)uVar5 ^ bVar2 ^
               ((byte)((int)uVar4 >> 7) | bVar2 * '\x02') ^ 99;
    }
    for (i = 0; i < 0x100; i = i + 1) {
      uVar3 = (uint)FSb[i];
      if ((FSb[i] & 0x80) == 0) {
        uVar5 = 0;
      }
      else {
        uVar5 = 0x1b;
      }
      uVar5 = (uVar5 ^ uVar3 * 2) & 0xff;
      FT0[i] = uVar3 << 8 ^ uVar5 ^ uVar3 << 0x10 ^ (uVar5 ^ uVar3) << 0x18;
      FT1[i] = FT0[i] << 8 | FT0[i] >> 0x18;
      FT2[i] = FT1[i] << 8 | FT1[i] >> 0x18;
      FT3[i] = FT2[i] << 8 | FT2[i] >> 0x18;
    }
    aes_tables_inited = 1;
  }
  return;
}



int aes_set_encryption_key(aes_context *ctx,uchar *key,uint keysize)

{
  int iVar1;
  uint32_t *RK;
  uint i;
  
  RK = ctx->rk;
  for (i = 0; i < keysize >> 2; i = i + 1) {
    RK[i] = CONCAT13(key[i * 4 + 3],CONCAT12(key[i * 4 + 2],CONCAT11(key[i * 4 + 1],key[i << 2])));
  }
  iVar1 = ctx->rounds;
  if (iVar1 == 0xe) {
    for (i = 0; i < 7; i = i + 1) {
      RK[8] = (uint)FSb[RK[7] & 0xff] << 0x18 ^
              *RK ^ RCON[i] ^ (uint)FSb[RK[7] >> 8 & 0xff] ^ (uint)FSb[RK[7] >> 0x10 & 0xff] << 8 ^
              (uint)FSb[RK[7] >> 0x18] << 0x10;
      RK[9] = RK[8] ^ RK[1];
      RK[10] = RK[9] ^ RK[2];
      RK[0xb] = RK[10] ^ RK[3];
      RK[0xc] = (uint)FSb[RK[0xb] >> 0x18] << 0x18 ^
                RK[4] ^ (uint)FSb[RK[0xb] & 0xff] ^ (uint)FSb[RK[0xb] >> 8 & 0xff] << 8 ^
                (uint)FSb[RK[0xb] >> 0x10 & 0xff] << 0x10;
      RK[0xd] = RK[0xc] ^ RK[5];
      RK[0xe] = RK[0xd] ^ RK[6];
      RK[0xf] = RK[0xe] ^ RK[7];
      RK = RK + 8;
    }
  }
  else {
    if (0xe < iVar1) {
      return -1;
    }
    if (iVar1 == 10) {
      for (i = 0; i < 10; i = i + 1) {
        RK[4] = (uint)FSb[RK[3] & 0xff] << 0x18 ^
                *RK ^ RCON[i] ^ (uint)FSb[RK[3] >> 8 & 0xff] ^ (uint)FSb[RK[3] >> 0x10 & 0xff] << 8
                ^ (uint)FSb[RK[3] >> 0x18] << 0x10;
        RK[5] = RK[4] ^ RK[1];
        RK[6] = RK[5] ^ RK[2];
        RK[7] = RK[6] ^ RK[3];
        RK = RK + 4;
      }
    }
    else {
      if (iVar1 != 0xc) {
        return -1;
      }
      for (i = 0; i < 8; i = i + 1) {
        RK[6] = (uint)FSb[RK[5] & 0xff] << 0x18 ^
                *RK ^ RCON[i] ^ (uint)FSb[RK[5] >> 8 & 0xff] ^ (uint)FSb[RK[5] >> 0x10 & 0xff] << 8
                ^ (uint)FSb[RK[5] >> 0x18] << 0x10;
        RK[7] = RK[6] ^ RK[1];
        RK[8] = RK[7] ^ RK[2];
        RK[9] = RK[8] ^ RK[3];
        RK[10] = RK[9] ^ RK[4];
        RK[0xb] = RK[10] ^ RK[5];
        RK = RK + 6;
      }
    }
  }
  return 0;
}



int aes_setkey(aes_context *ctx,int mode,uchar *key,uint keysize)

{
  int iVar1;
  
  if (aes_tables_inited == 0) {
    return -1;
  }
  ctx->mode = mode;
  ctx->rk = ctx->buf;
  if (keysize == 0x20) {
    ctx->rounds = 0xe;
  }
  else {
    if (0x20 < keysize) {
      return -1;
    }
    if (keysize == 0x10) {
      ctx->rounds = 10;
    }
    else {
      if (keysize != 0x18) {
        return -1;
      }
      ctx->rounds = 0xc;
    }
  }
  iVar1 = aes_set_encryption_key(ctx,key,keysize);
  return iVar1;
}



int aes_cipher(aes_context *ctx,uchar *input,uchar *output)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  byte bVar10;
  byte bVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  byte bVar15;
  uint32_t uVar16;
  uint32_t uVar17;
  uint32_t uVar18;
  uint32_t uVar19;
  uint *puVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  uint32_t Y3;
  uint32_t Y2;
  uint32_t Y1;
  uint32_t Y0;
  uint32_t X3;
  uint32_t X2;
  uint32_t X1;
  uint32_t X0;
  uint32_t *RK;
  int i;
  
  puVar20 = ctx->rk;
  X0 = *(uint *)input ^ *puVar20;
  X1 = *(uint *)(input + 4) ^ puVar20[1];
  X2 = *(uint *)(input + 8) ^ puVar20[2];
  RK = puVar20 + 4;
  X3 = *(uint *)(input + 0xc) ^ puVar20[3];
  i = ctx->rounds >> 1;
  while (i = i + -1, 0 < i) {
    uVar21 = FT3[X3 >> 0x18] ^ *RK ^ FT0[X0 & 0xff] ^ FT1[X1 >> 8 & 0xff] ^ FT2[X2 >> 0x10 & 0xff];
    uVar22 = FT3[X0 >> 0x18] ^ RK[1] ^ FT0[X1 & 0xff] ^ FT1[X2 >> 8 & 0xff] ^ FT2[X3 >> 0x10 & 0xff]
    ;
    uVar23 = FT3[X1 >> 0x18] ^ RK[2] ^ FT0[X2 & 0xff] ^ FT1[X3 >> 8 & 0xff] ^ FT2[X0 >> 0x10 & 0xff]
    ;
    uVar24 = FT3[X2 >> 0x18] ^ RK[3] ^ FT0[X3 & 0xff] ^ FT1[X0 >> 8 & 0xff] ^ FT2[X1 >> 0x10 & 0xff]
    ;
    X0 = FT3[uVar24 >> 0x18] ^
         RK[4] ^ FT0[uVar21 & 0xff] ^ FT1[uVar22 >> 8 & 0xff] ^ FT2[uVar23 >> 0x10 & 0xff];
    X1 = FT3[uVar21 >> 0x18] ^
         RK[5] ^ FT0[uVar22 & 0xff] ^ FT1[uVar23 >> 8 & 0xff] ^ FT2[uVar24 >> 0x10 & 0xff];
    puVar20 = RK + 7;
    X2 = FT3[uVar22 >> 0x18] ^
         RK[6] ^ FT0[uVar23 & 0xff] ^ FT1[uVar24 >> 8 & 0xff] ^ FT2[uVar21 >> 0x10 & 0xff];
    RK = RK + 8;
    X3 = FT3[uVar23 >> 0x18] ^
         *puVar20 ^ FT0[uVar24 & 0xff] ^ FT1[uVar21 >> 8 & 0xff] ^ FT2[uVar22 >> 0x10 & 0xff];
  }
  uVar21 = FT3[X3 >> 0x18] ^ *RK ^ FT0[X0 & 0xff] ^ FT1[X1 >> 8 & 0xff] ^ FT2[X2 >> 0x10 & 0xff];
  uVar22 = FT3[X0 >> 0x18] ^ RK[1] ^ FT0[X1 & 0xff] ^ FT1[X2 >> 8 & 0xff] ^ FT2[X3 >> 0x10 & 0xff];
  uVar23 = FT3[X1 >> 0x18] ^ RK[2] ^ FT0[X2 & 0xff] ^ FT1[X3 >> 8 & 0xff] ^ FT2[X0 >> 0x10 & 0xff];
  uVar24 = FT3[X2 >> 0x18] ^ RK[3] ^ FT0[X3 & 0xff] ^ FT1[X0 >> 8 & 0xff] ^ FT2[X1 >> 0x10 & 0xff];
  uVar16 = RK[4];
  bVar1 = FSb[uVar22 >> 8 & 0xff];
  bVar2 = FSb[uVar23 >> 0x10 & 0xff];
  bVar3 = FSb[uVar24 >> 0x18];
  uVar17 = RK[5];
  bVar4 = FSb[uVar22 & 0xff];
  bVar5 = FSb[uVar23 >> 8 & 0xff];
  bVar6 = FSb[uVar24 >> 0x10 & 0xff];
  bVar7 = FSb[uVar21 >> 0x18];
  uVar18 = RK[6];
  bVar8 = FSb[uVar23 & 0xff];
  bVar9 = FSb[uVar24 >> 8 & 0xff];
  bVar10 = FSb[uVar21 >> 0x10 & 0xff];
  bVar11 = FSb[uVar22 >> 0x18];
  uVar19 = RK[7];
  bVar12 = FSb[uVar24 & 0xff];
  bVar13 = FSb[uVar21 >> 8 & 0xff];
  bVar14 = FSb[uVar22 >> 0x10 & 0xff];
  bVar15 = FSb[uVar23 >> 0x18];
  *output = (byte)uVar16 ^ FSb[uVar21 & 0xff];
  output[1] = (byte)(uVar16 >> 8) ^ bVar1;
  output[2] = (byte)(uVar16 >> 0x10) ^ bVar2;
  output[3] = bVar3 ^ (byte)(uVar16 >> 0x18);
  output[4] = (byte)uVar17 ^ bVar4;
  output[5] = (byte)(uVar17 >> 8) ^ bVar5;
  output[6] = (byte)(uVar17 >> 0x10) ^ bVar6;
  output[7] = bVar7 ^ (byte)(uVar17 >> 0x18);
  output[8] = (byte)uVar18 ^ bVar8;
  output[9] = (byte)(uVar18 >> 8) ^ bVar9;
  output[10] = (byte)(uVar18 >> 0x10) ^ bVar10;
  output[0xb] = bVar11 ^ (byte)(uVar18 >> 0x18);
  output[0xc] = (byte)uVar19 ^ bVar12;
  output[0xd] = (byte)(uVar19 >> 8) ^ bVar13;
  output[0xe] = (byte)(uVar19 >> 0x10) ^ bVar14;
  output[0xf] = bVar15 ^ (byte)(uVar19 >> 0x18);
  return 0;
}



int gcm_initialize(void)

{
  aes_init_keygen_tables();
  return 0;
}



void gcm_mult(gcm_context *ctx,uchar *x,uchar *output)

{
  ulong uVar1;
  uchar rem;
  uchar hi;
  uchar lo;
  uint64_t zl;
  uint64_t zh;
  int i;
  
  zh = ctx->HH[(int)(uint)(x[0xf] & 0xf)];
  zl = ctx->HL[(int)(uint)(x[0xf] & 0xf)];
  for (i = 0xf; -1 < i; i = i + -1) {
    if (i != 0xf) {
      uVar1 = zh << 0x3c;
      zh = zh >> 4 ^ last4[(int)(uint)((byte)zl & 0xf)] << 0x30 ^ ctx->HH[(int)(uint)(x[i] & 0xf)];
      zl = (zl >> 4 | uVar1) ^ ctx->HL[(int)(uint)(x[i] & 0xf)];
    }
    uVar1 = zh << 0x3c;
    zh = zh >> 4 ^ last4[(int)(uint)((byte)zl & 0xf)] << 0x30 ^ ctx->HH[(int)(uint)(x[i] >> 4)];
    zl = (zl >> 4 | uVar1) ^ ctx->HL[(int)(uint)(x[i] >> 4)];
  }
  *output = (uchar)(zh >> 0x38);
  output[1] = (uchar)(zh >> 0x30);
  output[2] = (uchar)(zh >> 0x28);
  output[3] = (uchar)(zh >> 0x20);
  output[4] = (uchar)(zh >> 0x18);
  output[5] = (uchar)(zh >> 0x10);
  output[6] = (uchar)(zh >> 8);
  output[7] = (uchar)zh;
  output[8] = (uchar)(zl >> 0x38);
  output[9] = (uchar)(zl >> 0x30);
  output[10] = (uchar)(zl >> 0x28);
  output[0xb] = (uchar)(zl >> 0x20);
  output[0xc] = (uchar)(zl >> 0x18);
  output[0xd] = (uchar)(zl >> 0x10);
  output[0xe] = (uchar)(zl >> 8);
  output[0xf] = (byte)zl;
  return;
}



int gcm_setkey(gcm_context *ctx,uchar *key,uint keysize)

{
  ulong uVar1;
  ulong uVar2;
  int iVar3;
  uint uVar4;
  uchar h [16];
  uint32_t T;
  uint64_t *HiH;
  uint64_t *HiL;
  uint64_t lo;
  uint64_t hi;
  int ret;
  uint64_t vh;
  uint64_t vl;
  int j;
  int i;
  
  memset(ctx,0,0x268);
  memset(h,0,0x10);
  iVar3 = aes_setkey(&ctx->aes_ctx,1,key,keysize);
  if ((iVar3 == 0) && (iVar3 = aes_cipher(&ctx->aes_ctx,h,h), iVar3 == 0)) {
    vh = CONCAT44((uint)h[3] | (uint)h[0] << 0x18 | (uint)h[1] << 0x10 | (uint)h[2] << 8,
                  (uint)h[7] | (uint)h[4] << 0x18 | (uint)h[5] << 0x10 | (uint)h[6] << 8);
    vl = CONCAT44((uint)h[11] | (uint)h[8] << 0x18 | (uint)h[9] << 0x10 | (uint)h[10] << 8,
                  (uint)h[15] | (uint)h[12] << 0x18 | (uint)h[13] << 0x10 | (uint)h[14] << 8);
    ctx->HL[8] = vl;
    ctx->HH[8] = vh;
    ctx->HH[0] = 0;
    ctx->HL[0] = 0;
    for (i = 4; i != 0; i = i >> 1) {
      uVar4 = (uint)vl;
      vl = vl >> 1 | vh << 0x3f;
      vh = (ulong)((uVar4 & 1) * -0x1f000000) << 0x20 ^ vh >> 1;
      ctx->HL[i] = vl;
      ctx->HH[i] = vh;
    }
    for (i = 2; i < 0x10; i = i << 1) {
      uVar1 = ctx->HH[i];
      uVar2 = ctx->HL[i];
      for (j = 1; j < i; j = j + 1) {
        (ctx->HH + i)[j] = ctx->HH[j] ^ uVar1;
        (ctx->HL + i)[j] = ctx->HL[j] ^ uVar2;
      }
    }
    iVar3 = 0;
  }
  return iVar3;
}



int gcm_start(gcm_context *ctx,int mode,uchar *iv,size_t iv_len,uchar *add,size_t add_len)

{
  int iVar1;
  ulong uVar2;
  ulong local_68;
  ulong local_58;
  uchar work_buf [16];
  int ret;
  size_t use_len;
  size_t i;
  uchar *p;
  
  memset(ctx->y,0,0x10);
  memset(ctx->buf,0,0x10);
  ctx->len = 0;
  ctx->add_len = 0;
  ctx->mode = mode;
  (ctx->aes_ctx).mode = 1;
  if (iv_len == 0xc) {
    memcpy(ctx->y,iv,0xc);
    ctx->y[0xf] = '\x01';
  }
  else {
    memset(work_buf,0,0x10);
    work_buf[12] = (uchar)((iv_len << 3) >> 0x18);
    work_buf[13] = (uchar)((iv_len << 3) >> 0x10);
    work_buf[14] = (uchar)((iv_len << 3) >> 8);
    work_buf[15] = (uchar)((int)iv_len << 3);
    p = iv;
    for (local_58 = iv_len; local_58 != 0; local_58 = local_58 - uVar2) {
      uVar2 = 0x10;
      if (local_58 < 0x11) {
        uVar2 = local_58;
      }
      for (i = 0; i < uVar2; i = i + 1) {
        ctx->y[i] = ctx->y[i] ^ p[i];
      }
      gcm_mult(ctx,ctx->y,ctx->y);
      p = p + uVar2;
    }
    for (i = 0; i < 0x10; i = i + 1) {
      ctx->y[i] = ctx->y[i] ^ work_buf[i];
    }
    gcm_mult(ctx,ctx->y,ctx->y);
  }
  iVar1 = aes_cipher(&ctx->aes_ctx,ctx->y,ctx->base_ectr);
  if (iVar1 == 0) {
    ctx->add_len = add_len;
    p = add;
    for (local_68 = add_len; local_68 != 0; local_68 = local_68 - uVar2) {
      uVar2 = 0x10;
      if (local_68 < 0x11) {
        uVar2 = local_68;
      }
      for (i = 0; i < uVar2; i = i + 1) {
        ctx->buf[i] = ctx->buf[i] ^ p[i];
      }
      gcm_mult(ctx,ctx->buf,ctx->buf);
      p = p + uVar2;
    }
    iVar1 = 0;
  }
  return iVar1;
}



int gcm_update(gcm_context *ctx,size_t length,uchar *input,uchar *output)

{
  int iVar1;
  ulong uVar2;
  uchar *local_58;
  uchar *local_50;
  ulong local_48;
  uchar ectr [16];
  int ret;
  size_t use_len;
  size_t i;
  
  ctx->len = ctx->len + length;
  local_58 = output;
  local_50 = input;
  local_48 = length;
  while( true ) {
    if (local_48 == 0) {
      return 0;
    }
    uVar2 = 0x10;
    if (local_48 < 0x11) {
      uVar2 = local_48;
    }
    for (i = 0x10;
        (0xc < i &&
        (ctx->base_ectr[i + 0xf] = ctx->base_ectr[i + 0xf] + '\x01', ctx->base_ectr[i + 0xf] == '\0'
        )); i = i - 1) {
    }
    iVar1 = aes_cipher(&ctx->aes_ctx,ctx->y,ectr);
    if (iVar1 != 0) break;
    if (ctx->mode == 1) {
      for (i = 0; i < uVar2; i = i + 1) {
        local_58[i] = ectr[i] ^ local_50[i];
        ctx->buf[i] = ctx->buf[i] ^ local_58[i];
      }
    }
    else {
      for (i = 0; i < uVar2; i = i + 1) {
        ctx->buf[i] = ctx->buf[i] ^ local_50[i];
        local_58[i] = ectr[i] ^ local_50[i];
      }
    }
    gcm_mult(ctx,ctx->buf,ctx->buf);
    local_48 = local_48 - uVar2;
    local_50 = local_50 + uVar2;
    local_58 = local_58 + uVar2;
  }
  return iVar1;
}



int gcm_finish(gcm_context *ctx,uchar *tag,size_t tag_len)

{
  long lVar1;
  long lVar2;
  uchar work_buf [16];
  uint64_t orig_add_len;
  uint64_t orig_len;
  size_t i;
  
  lVar1 = ctx->len << 3;
  lVar2 = ctx->add_len << 3;
  if (tag_len != 0) {
    memcpy(tag,ctx->base_ectr,tag_len);
  }
  if ((lVar1 != 0) || (lVar2 != 0)) {
    memset(work_buf,0,0x10);
    work_buf[0] = (uchar)((ulong)lVar2 >> 0x38);
    work_buf[1] = (uchar)((ulong)lVar2 >> 0x30);
    work_buf[2] = (uchar)((ulong)lVar2 >> 0x28);
    work_buf[3] = (uchar)((ulong)lVar2 >> 0x20);
    work_buf[4] = (uchar)((ulong)lVar2 >> 0x18);
    work_buf[5] = (uchar)((ulong)lVar2 >> 0x10);
    work_buf[6] = (uchar)((ulong)lVar2 >> 8);
    work_buf[7] = (uchar)lVar2;
    work_buf[8] = (uchar)((ulong)lVar1 >> 0x38);
    work_buf[9] = (uchar)((ulong)lVar1 >> 0x30);
    work_buf[10] = (uchar)((ulong)lVar1 >> 0x28);
    work_buf[11] = (uchar)((ulong)lVar1 >> 0x20);
    work_buf[12] = (uchar)((ulong)lVar1 >> 0x18);
    work_buf[13] = (uchar)((ulong)lVar1 >> 0x10);
    work_buf[14] = (uchar)((ulong)lVar1 >> 8);
    work_buf[15] = (uchar)lVar1;
    for (i = 0; i < 0x10; i = i + 1) {
      ctx->buf[i] = ctx->buf[i] ^ work_buf[i];
    }
    gcm_mult(ctx,ctx->buf,ctx->buf);
    for (i = 0; i < tag_len; i = i + 1) {
      tag[i] = tag[i] ^ ctx->buf[i];
    }
  }
  return 0;
}



int gcm_crypt_and_tag(gcm_context *ctx,int mode,uchar *iv,size_t iv_len,uchar *add,size_t add_len,
                     uchar *input,uchar *output,size_t length,uchar *tag,size_t tag_len)

{
  gcm_start(ctx,mode,iv,iv_len,add,add_len);
  gcm_update(ctx,length,input,output);
  gcm_finish(ctx,tag,tag_len);
  return 0;
}



int gcm_auth_decrypt(gcm_context *ctx,uchar *iv,size_t iv_len,uchar *add,size_t add_len,uchar *input
                    ,uchar *output,size_t length,uchar *tag,size_t tag_len)

{
  int iVar1;
  uchar check_tag [16];
  size_t i;
  int diff;
  
  gcm_crypt_and_tag(ctx,0,iv,iv_len,add,add_len,input,output,length,check_tag,tag_len);
  diff = 0;
  for (i = 0; i < tag_len; i = i + 1) {
    diff = diff | (uint)(check_tag[i] ^ tag[i]);
  }
  if (diff == 0) {
    iVar1 = 0;
  }
  else {
    memset(output,0,length);
    iVar1 = 0x55555555;
  }
  return iVar1;
}



void gcm_zero_ctx(gcm_context *ctx)

{
  memset(ctx,0,0x268);
  return;
}



int aes_gcm_encrypt(uchar *output,uchar *input,int input_length,uchar *key,size_t key_len,uchar *iv,
                   size_t iv_len)

{
  int iVar1;
  gcm_context ctx;
  uchar *tag_buf;
  size_t tag_len;
  int ret;
  
  gcm_setkey(&ctx,key,(uint)key_len);
  iVar1 = gcm_crypt_and_tag(&ctx,1,iv,iv_len,(uchar *)0x0,0,input,output,(long)input_length,
                            (uchar *)0x0,0);
  gcm_zero_ctx(&ctx);
  return iVar1;
}



int aes_gcm_decrypt(uchar *output,uchar *input,int input_length,uchar *key,size_t key_len,uchar *iv,
                   size_t iv_len)

{
  int iVar1;
  gcm_context ctx;
  uchar *tag_buf;
  size_t tag_len;
  int ret;
  
  gcm_setkey(&ctx,key,(uint)key_len);
  iVar1 = gcm_crypt_and_tag(&ctx,0,iv,iv_len,(uchar *)0x0,0,input,output,(long)input_length,
                            (uchar *)0x0,0);
  fwrite("decrypted\n",1,10,stderr);
  gcm_zero_ctx(&ctx);
  return iVar1;
}



void _fini(void)

{
  return;
}


