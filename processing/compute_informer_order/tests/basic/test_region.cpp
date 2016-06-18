
#include <boost/test/unit_test.hpp>
#include "../../neutron/region.h"


BOOST_AUTO_TEST_SUITE(region)

BOOST_AUTO_TEST_CASE(read)
{
    auto& region_manager = neutron::Region::objects();
    BOOST_CHECK_EQUAL(region_manager.all().count(), 3);
}

BOOST_AUTO_TEST_SUITE_END()
