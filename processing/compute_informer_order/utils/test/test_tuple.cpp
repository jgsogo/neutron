#define BOOST_TEST_MODULE utils_tests
#include <boost/test/unit_test.hpp>

#include "print_helper.hpp"
#include "../tuple.h"


BOOST_AUTO_TEST_CASE(tuple_projection)
{
    // Compile time definitions
    typedef std::tuple<int, std::string, float> mytuple;
    constexpr std::size_t index_int = ::utils::tuple::index<int, int, std::string, float>();
    constexpr std::size_t index_string = ::utils::tuple::index<std::string, int, std::string, float>();
    constexpr std::size_t index_float = ::utils::tuple::index<float, int, std::string, float>();

    // Tests
    mytuple a{2, "hola", 0.f};

    BOOST_CHECK_EQUAL(::utils::tuple::project<index_int>(a), std::tuple<int>(2));
    BOOST_CHECK_EQUAL(::utils::tuple::project<index_string>(a), std::tuple<std::string>("hola"));
    BOOST_CHECK_EQUAL(::utils::tuple::project<index_float>(a), std::tuple<float>(0.f));
}

BOOST_AUTO_TEST_CASE(PassTest)
{
    BOOST_CHECK_EQUAL(4, 4);
}