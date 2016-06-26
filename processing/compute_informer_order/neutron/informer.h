
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "region.h"

namespace neutron {

    class InformerManager;

    class Informer : public qs::BaseModel<Informer, informer_id, Region, float> {
        using BaseModel = qs::BaseModel<Informer, informer_id, Region, float>;
    public:
        Informer();
        Informer(const BaseModel::tuple& data);
        virtual ~Informer() {};

        virtual void print(std::ostream& os) const {
            os << "Informer[" << pk() << "]";
        }

        const float get_confidence() const;

        // with a custom manager
        static InformerManager& objects();
    };

    class InformerManager : public BaseManager<Informer> {
        public:
            InformerManager();
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
