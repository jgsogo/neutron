
#pragma once

#include "queryset/models/manager.h"

namespace neutron {

    template <typename... Args>
    class BaseManager : public qs::FileManager<Args...> {
        public:
            BaseManager(const std::string& filename) : qs::FileManager<Args...>(filename) {}

    };

}
