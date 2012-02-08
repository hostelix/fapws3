#include <ev.h>
#include <Python.h>


#define MAXHEADER 4096

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#else
#define PyBytes_AsString PyString_AsString 
#define PyBytes_FromString PyString_FromString 
#define PyBytes_FromStringAndSize PyString_FromStringAndSize 
#define PyBytes_FromFormat PyString_FromFormat 
#define PyLong_FromString PyInt_FromString 
#define PyLong_FromLong PyInt_FromLong 
#define PyBytes_Concat PyString_Concat 
#define PyBytes_FromStringAndSize PyBuffer_FromMemory 
#define PyBytes_AsStringAndSize PyObject_AsReadBuffer 
#define PyObject_Bytes PyObject_Str 
#define PyUnicode_FromString PyString_FromString
#endif 


/*
Structure we use for each client's connection. 
*/
struct client {
        int fd;
        ev_io ev_write;
        ev_io ev_read;
        char *remote_addr;
        int remote_port;
        char *input_header;
        char *input_body;
        size_t input_pos;
        int retry;
        char *uri;
        char *cmd;
        char *http_major_minor;
        char *uri_path;   //correspond to the registered uri_header 
        PyObject *wsgi_cb;
        int response_iter_sent; //-2: nothing sent, -1: header sent, 0-9999: iter sent
        char response_header[MAXHEADER];
        int response_header_length;
        PyObject *response_content;
        PyObject *response_content_obj;
        FILE *response_fp; // file of the sent file
};

struct TimerObj {
        ev_timer timerwatcher;
        float delay;
        PyObject *py_cb;
};


