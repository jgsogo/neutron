
#include <boost/test/unit_test.hpp>
#include "../../entropy.h"


BOOST_AUTO_TEST_SUITE(entropy)

BOOST_AUTO_TEST_CASE(compute_information)
{
    BOOST_CHECK_EQUAL(utils::compute_information(0), 0);
    BOOST_CHECK_EQUAL(utils::compute_information(1), 0);  // probability equals 1 ==> always happen
    BOOST_CHECK_EQUAL(utils::compute_information(0.5), 0.5);
}

BOOST_AUTO_TEST_CASE(compute_entropy)
{
    std::map<std::string, std::size_t> data = {{"a", 0}};
    BOOST_CHECK_EQUAL(utils::compute_entropy(data), 0);

    data["b"] = 1;
    BOOST_CHECK_EQUAL(utils::compute_entropy(data), 0);

    data["c"] = 1;
    BOOST_CHECK_EQUAL(utils::compute_entropy(data), 1);

    data["d"] = 1;
    BOOST_CHECK_CLOSE(utils::compute_entropy(data), -3.f*(1.f/3.f)*std::log2(1.f/3.f), 0.00001);  // According to shannon entropy
}

BOOST_AUTO_TEST_SUITE_END()
