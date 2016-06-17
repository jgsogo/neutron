
#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>

#include "../../neutron/region.h"
#include "../config_tests.h"

BOOST_AUTO_TEST_SUITE(region)

BOOST_AUTO_TEST_CASE(read)
{
    namespace fs = boost::filesystem;
    fs::path full_path = test_data_dir / fs::path("region.tsv");
    
    auto& region_manager = neutron::Region::objects(full_path.string());
    BOOST_CHECK_EQUAL(region_manager.all().count(), 3);
}

BOOST_AUTO_TEST_SUITE_END()
