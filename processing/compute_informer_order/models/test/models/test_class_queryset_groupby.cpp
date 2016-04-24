
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

    BOOST_AUTO_TEST_CASE(group_by_single)
    {
        QuerySet<int, std::string, float> qs(initial_qs);
        auto f4 = qs.groupBy<int>();
        BOOST_CHECK_EQUAL(f4.size(), 3);

        const ::utils::queryset<int, std::string, float>& f4_int0 = f4.find(0)->second;
        BOOST_CHECK_EQUAL(f4_int0.size(), 3);
    }

    BOOST_AUTO_TEST_CASE(group_by_compound)
    {
        QuerySet<int, std::string, float> qs(initial_qs);
        auto f4 = qs.groupBy<int, std::string>();
        BOOST_CHECK_EQUAL(f4.size(), 9);

        const std::tuple<int, std::string>& f4_key = f4.find(std::tuple<int, std::string>{0, "hola"})->first;
        const ::utils::queryset<int, std::string, float>& f4_value = f4.find(std::tuple<int, std::string>{0, "hola"})->second;
        BOOST_CHECK_EQUAL(f4_value.size(), 1);
    }

BOOST_AUTO_TEST_SUITE_END()

