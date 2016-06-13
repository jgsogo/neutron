
#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>

#include "../../neutron/region.h"
#include "../config_tests.h"


BOOST_AUTO_TEST_SUITE(region)

BOOST_AUTO_TEST_CASE(read)
{
    namespace fs = boost::filesystem;
    fs::path full_path = test_data_dir / fs::path("region.tsv");

    neutron::RegionManager regions(full_path.string());
    BOOST_CHECK_EQUAL(regions.count(), 1);

}

BOOST_AUTO_TEST_SUITE_END()
