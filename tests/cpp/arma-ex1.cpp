// File generated on Thu Aug 21, 2014 06:00:18 PM by xcpp.
#define XC_CPP
#include <armadillo>
#include <xc>


namespace excentury {
XC_DUMP_TEMPLATED_TENSOR(class elementType, arma::Mat<elementType>, m, m.mem[0]) {
    size_t ndims = 2;
    unsigned char rm = 0;
    XC_BYTE(rm);
    XC_SIZE(ndims);
    size_t size = m.n_elem;
    size_t dim[2] = {m.n_rows, m.n_cols};
    XC_ARRAY(dim, ndims);
    XC_ARRAY(m.mem, size);
}
XC_LOAD_TEMPLATED_TENSOR(class elementType, arma::Mat<elementType>, m) {
    size_t ndims;
    unsigned char rm;
    XC_BYTE(rm);
    if (rm != 0) {
        char msg[500];
        sprintf(msg, "Armadillo Mat::load:\n"
                "    RM mismatch, got %d, needs %d.", rm, 0);
        excentury::error(msg);
    }
    XC_SIZE(ndims);
    if (ndims != 2) {
        char msg[500];
        sprintf(msg, "Armadillo Mat::load('%s'):\n" \
                "    dimension mismatch, needs dim = 2", varname);
        excentury::error(msg);
    }
    size_t* dim = new size_t[ndims];
    XC_ARRAY(dim, ndims);
    m.resize(dim[0], dim[1]);
    elementType* mem = const_cast<elementType*>(m.mem);
    XC_ARRAY(mem, m.n_elem);
    delete [] dim;
}
}
void xc_help() {
    fprintf(stderr,
    "program: arma-ex1\n"
    "\ndescription:\n"
    "    Armadillo example 2: Computes the determinant and inverse of a\n"
    "    matrix.\n"
    "\nparameters:\n"
    "    `A`: input matrix\n"
    "\n");
}
void xc_input() {
    xc_help();
    excentury::TextInterface<excentury::dump_mode> XC_DI_(stdout);
    arma::mat A(2, 2); XC_DI_.dump(A, "A", A(0,0));
    XC_DI_.close();
}
int main(int argc, char** argv) {
    /*Armadillo example 2: Computes the determinant and inverse of a
    matrix.*/
    excentury::check_inputs(argc);
    excentury::print_help(argv, xc_help);
    excentury::print_inputs(argv, xc_input);
    excentury::STextInterface<excentury::load_mode> XC_LI_(argv[1]);
    arma::mat A(2, 2); XC_LI_.load(A, A(0,0));
    XC_LI_.close();

    double d = det(A);
    arma::mat Ainv;
    try {
        Ainv = inv(A);
    } catch (std::runtime_error& run_error) {
        excentury::error(run_error.what());
    }

    excentury::TextInterface<excentury::dump_mode> XC_DI_(stdout);
    XC_DI_.dump(d, "detA");
    XC_DI_.dump(Ainv, "Ainv", Ainv(0, 0));
    XC_DI_.close();
}

