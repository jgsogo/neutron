
#include <boost/test/unit_test.hpp>

#include "print_helper.hpp"
#include "../../queryset.h"


typedef ::utils::queryset<int, std::string, float> myqueryset;
typedef std::tuple<int, std::string, float> mytuple;

struct Fixture {
    Fixture() {
        initial_qs.push_back(mytuple{ 0, "hola", 0.f });
        initial_qs.push_back(mytuple{ 0, "bye", 0.1f });
        initial_qs.push_back(mytuple{ 0, "ciao", 0.2f });
        
        initial_qs.push_back(mytuple{ 1, "hola", 1.f });
        initial_qs.push_back(mytuple{ 1, "bye", 1.1f });
        initial_qs.push_back(mytuple{ 1, "ciao", 1.2f });
        
        initial_qs.push_back(mytuple{ 2, "hola", 2.f });
        initial_qs.push_back(mytuple{ 2, "bye", 2.1f });
        initial_qs.push_back(mytuple{ 2, "ciao", 2.2f });
    }
    ~Fixture() {}

    myqueryset initial_qs;
};

BOOST_FIXTURE_TEST_SUITE(queryset_class, Fixture)

BOOST_AUTO_TEST_CASE(filter_int)
{
    QuerySet<int, std::string, float> qs(initial_qs);
    auto f1 = qs.filter(0).get();
    BOOST_CHECK_EQUAL(f1.size(), 3);
}

BOOST_AUTO_TEST_CASE(filter_concat)
{
    QuerySet<int, std::string, float> qs(initial_qs);
    auto f2 = qs.filter(0).filter<std::string>("hola").get();
    BOOST_CHECK_EQUAL(f2.size(), 1);
}

BOOST_AUTO_TEST_CASE(filter_empty)
{
    QuerySet<int, std::string, float> qs(initial_qs);
    auto f3 = qs.filter(0).filter(1).get();
    BOOST_CHECK_EQUAL(f3.size(), 0);
}

BOOST_AUTO_TEST_CASE(filter_tuple)
{
    QuerySet<int, std::string, float> qs(initial_qs);
    auto f4 = qs.filter(std::make_tuple<int, std::string>(0, "hola")).get();
    BOOST_CHECK_EQUAL(f4.size(), 1);
}

BOOST_AUTO_TEST_SUITE_END()
