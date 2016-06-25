
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "manager.h"

namespace neutron {

    class RegionManager;

    class Region : public qs::BaseModel<Region, region_id, region_id, std::string> {
        using BaseModel = qs::BaseModel<Region, region_id, region_id, std::string>;
        public:
            Region();
            Region(const Region& other);
            Region(const BaseModel::tuple& data);
            virtual ~Region() {};

            virtual void print(std::ostream& os) const {
                this->eval(); // To retrieve name (if not already retrieved)
                os << std::get<2>(_data);
            }

            // with a custom manager
            static RegionManager& objects();
        protected:
    };

    class RegionManager : public BaseManager<Region> {
        public:
            RegionManager();
    };
}
/*
template<class Ch, class Tr>
std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os, const neutron::Region& rhs) {
    rhs.serialize(os);
    return os;
}
*/
