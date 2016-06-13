
#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>

#include "../../neutron/informer.h"
#include "../config_tests.h"


BOOST_AUTO_TEST_SUITE(informer)

BOOST_AUTO_TEST_CASE(read)
{
    namespace fs = boost::filesystem;
    fs::path full_path = test_data_dir / fs::path("data_informers.tsv");

    neutron::InformerManager informers(full_path.string());
    //auto spaniards = informers.get_by_region(neutron::region_id)

}

BOOST_AUTO_TEST_SUITE_END()
