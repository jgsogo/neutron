#define BOOST_TEST_MODULE utils_tests
#include <boost/test/unit_test.hpp>

#include "print_helper.hpp"
#include "../tuple.h"

BOOST_AUTO_TEST_CASE(tuple_index)
{
    typedef std::tuple<int, std::string, float> mytuple;
    BOOST_CHECK_EQUAL((::utils::tuple::index<int, int, std::string, float>()), 0);
    BOOST_CHECK_EQUAL((::utils::tuple::index<std::string, int, std::string, float>()), 1);
    BOOST_CHECK_EQUAL((::utils::tuple::index<float, int, std::string, float>()), 2);
}

BOOST_AUTO_TEST_CASE(tuple_projection)
{
    typedef std::tuple<int, std::string, float> mytuple;
    mytuple a{2, "hola", 0.f};

    // Indexes for each element
    constexpr std::size_t index_int = ::utils::tuple::index<int, int, std::string, float>();
    constexpr std::size_t index_string = ::utils::tuple::index<std::string, int, std::string, float>();
    constexpr std::size_t index_float = ::utils::tuple::index<float, int, std::string, float>();

    // Basic functions: 'head' and 'tail'
    BOOST_CHECK_EQUAL(::utils::tuple::head(a), 2);
    BOOST_CHECK_EQUAL(::utils::tuple::tail(a), (std::tuple<std::string, float>("hola", 0.f)));

    // Projection on one axis
    BOOST_CHECK_EQUAL(::utils::tuple::project<index_int>(a), std::tuple<int>(2));
    BOOST_CHECK_EQUAL(::utils::tuple::project<index_string>(a), std::tuple<std::string>("hola"));
    BOOST_CHECK_EQUAL(::utils::tuple::project<index_float>(a), std::tuple<float>(0.f));

    BOOST_CHECK_EQUAL(::utils::tuple::project<0>(a), std::tuple<int>(2));
    BOOST_CHECK_EQUAL(::utils::tuple::project<1>(a), std::tuple<std::string>("hola"));
    BOOST_CHECK_EQUAL(::utils::tuple::project<2>(a), std::tuple<float>(0.f));

    // Projection on several axis
    BOOST_CHECK_EQUAL((::utils::tuple::project<0, 1>(a)), (std::tuple<int, std::string>(2, "hola")));
    BOOST_CHECK_EQUAL((::utils::tuple::project<1, 2>(a)), (std::tuple<std::string, float>("hola", 0.f)));
    BOOST_CHECK_EQUAL((::utils::tuple::project<0, 2>(a)), (std::tuple<int, float>(2, 0.f)));

    // Unordered projection
    BOOST_CHECK_EQUAL((::utils::tuple::project<2, 0>(a)), (std::tuple<float, int>(0.f, 2)));
}

BOOST_AUTO_TEST_CASE(tuple_remove_ith_type)
{
    typedef std::tuple<int, std::string, float> mytuple;
    typedef ::utils::tuple::remove_ith_type<0, mytuple>::type mytuple_12;
    typedef ::utils::tuple::remove_ith_type<1, mytuple>::type mytuple_02;
    typedef ::utils::tuple::remove_ith_type<2, mytuple>::type mytuple_01;

    BOOST_CHECK_EQUAL((mytuple_12{ "a", 0.f }), (std::tuple<std::string, float>{"a", 0.f}));
    BOOST_CHECK_EQUAL((mytuple_02{ 0, 0.f }), (std::tuple<int, float>{0, 0.f}));
    BOOST_CHECK_EQUAL((mytuple_01{ 0, "a" }), (std::tuple<int, std::string>{0, "a"}));
}

BOOST_AUTO_TEST_CASE(tuple_gen_seq)
{
    typedef std::tuple<int, std::string, float> mytuple;
    mytuple a{ 2, "hola", 0.f };

    typedef ::utils::tuple::gen_seq<3, 0> seq1;
    typedef ::utils::tuple::gen_seq<3, 1> seq2;
    typedef ::utils::tuple::gen_seq<3, 2> seq3;

    // It's used to project
    BOOST_CHECK_EQUAL(::utils::tuple::project(a, seq1()), (std::tuple<std::string, float>("hola", 0.f)));
    BOOST_CHECK_EQUAL(::utils::tuple::project(a, seq2()), (std::tuple<int, float>(2, 0.f)));
    BOOST_CHECK_EQUAL(::utils::tuple::project(a, seq3()), (std::tuple<int, std::string>(2, "hola")));
    
    // This should give a compiler error
    typedef ::utils::tuple::gen_seq<3, 3> seq4;
    BOOST_CHECK_EQUAL(::utils::tuple::project(a, seq4()), a);
}

BOOST_AUTO_TEST_CASE(tuple_comparaison)
{
    typedef std::tuple<int, std::string, float> mytuple;
    mytuple a{ 2, "hola", 0.f };

    BOOST_CHECK_GT(a, (mytuple{ 1, "z", 23.f }));
    BOOST_CHECK_GT(a, (mytuple{ 2, "a", 23.f }));
    BOOST_CHECK_GT(a, (mytuple{ 2, "hola", -1.f }));
}

