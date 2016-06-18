
#include <boost/test/unit_test.hpp>

#include "../../neutron/informer.h"

BOOST_AUTO_TEST_SUITE(informer)

BOOST_AUTO_TEST_CASE(read)
{
    using namespace neutron;

    auto& informers = neutron::Informer::objects();
    BOOST_CHECK_EQUAL(informers.all().count(), 2);

    //auto& informers = neutron::Informer::objects(full_path.string());
    //BOOST_CHECK_EQUAL(informers.all().count(), 2);

}

BOOST_AUTO_TEST_SUITE_END()
