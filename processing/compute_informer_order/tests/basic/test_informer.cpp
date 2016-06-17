
#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>

#include "../../neutron/informer.h"
#include "../config_tests.h"


BOOST_AUTO_TEST_SUITE(informer)

BOOST_AUTO_TEST_CASE(read)
{
    using namespace neutron;
    namespace fs = boost::filesystem;
    fs::path full_path = test_data_dir / fs::path("data_informers.tsv");

    auto& informers = neutron::Informer::objects(full_path.string());
    BOOST_CHECK_EQUAL(informers.all().count(), 2);

}

BOOST_AUTO_TEST_SUITE_END()
