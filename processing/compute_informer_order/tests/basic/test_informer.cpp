
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

    typedef qs::Model<int, std::string, float> MyModel;
    MyModel m;
    auto& manager = m.objects(std::string("C:/Users/xe53859/src/queryset-cpp/tests/data/ex_filequeryset.tsv"));
    BOOST_CHECK_EQUAL(manager.all().count(), 3);


    /*
    typedef qs::Model<int, int, float> MyModel;
    MyModel m;
    auto& manager = m.objects(full_path.string());
    BOOST_CHECK_EQUAL(manager.all().count(), 2);
    */
    /*
    Informer m;
    auto& informers = m.objects(full_path.string());
    //informers.all();
    BOOST_CHECK_EQUAL(informers.all().count(), 2);
    */

    //auto& informers = neutron::Informer::objects(full_path.string());
    //BOOST_CHECK_EQUAL(informers.all().count(), 2);

}

BOOST_AUTO_TEST_SUITE_END()
