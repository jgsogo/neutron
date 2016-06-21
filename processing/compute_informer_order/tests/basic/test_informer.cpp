
#include <boost/test/unit_test.hpp>

#include "../../neutron/informer.h"

BOOST_AUTO_TEST_SUITE(informer)

BOOST_AUTO_TEST_CASE(read)
{
    using namespace neutron;

    auto& informers = neutron::Informer::objects();
    BOOST_CHECK_EQUAL(informers.all().count(), 2);

    auto i1 = informers.all()[0];
    BOOST_CHECK_EQUAL(std::get<0>(i1), informer_id(1));
    //BOOST_CHECK_EQUAL(std::get<1>(i1), Region(1));
    BOOST_CHECK_EQUAL(std::get<2>(i1), 0.2f);

}

BOOST_AUTO_TEST_SUITE_END()
