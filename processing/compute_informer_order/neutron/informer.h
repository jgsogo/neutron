
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "manager.h"
#include "region.h"

namespace neutron {

    class InformerManager : public BaseManager<informer_id, Region, float> {
        public:
            InformerManager();
    };

    class Informer : public qs::BaseModel<InformerManager> {
        using BaseModel = qs::BaseModel<InformerManager>;
        public:
            Informer();
            Informer(const InformerManager::tuple& data);
            virtual ~Informer() {};

    };
}
/*
template<class Ch, class Tr>
std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os,
    const neutron::Informer& rhs)
{
    rhs.serialize(os);
    return os;
}
*/
