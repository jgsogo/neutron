
#pragma once

#include "queryset/models/model.h"
#include "types.h"

namespace neutron {

    class Region : public qs::Model<region_id, region_id, std::string> {
        public:
            Region();
            Region(const std::tuple<region_id, region_id, std::string>& data);

        protected:
            region_id _id;
            region_id _parent;
            std::string _name;
    };

    /*
    class RegionManager {
        public:
            typedef QuerySet<region_id, region_id, std::string> QuerySet;

        public:
            RegionManager(const std::string& filename);
            ~RegionManager();

            QuerySet all() const;

        protected:
            class Impl;
            Impl* _impl;
    };

    class Region {
        public:
            Region();
            Region(const std::tuple<region_id, region_id, std::string>& data);
            static RegionManager objects(const std::string& filename) {
                // TODO: Manager as singleton?
                static RegionManager manager(filename);
                return manager;
            }

        protected:
            region_id _id;
            region_id _parent;
            std::string _name;
    };
    */
}
