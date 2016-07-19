
#include <boost/test/unit_test.hpp>
#include "../../entropy.h"


BOOST_AUTO_TEST_SUITE(entropy)

BOOST_AUTO_TEST_CASE(compute_information)
{
    BOOST_CHECK_EQUAL(utils::compute_information(0), 0);
    BOOST_CHECK_EQUAL(utils::compute_information(1), 0);
}

BOOST_AUTO_TEST_CASE(compute_entropy)
{
    std::map<std::string, std::size_t> data = {{"a", 0}, {"b", 1}};
    BOOST_CHECK_EQUAL(utils::compute_entropy(data), 0);
}

BOOST_AUTO_TEST_SUITE_END()
