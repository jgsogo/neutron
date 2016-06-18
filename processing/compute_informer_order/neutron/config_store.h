
#pragma once

#include <string>

namespace neutron {

    class ConfigStore {
        public:
            static ConfigStore& get();

            void parse_file(const std::string& filename);
            void parse_data(const std::string& data);

            template<typename T>
            T get_value_as(const std::string& key) const {
                std::stringstream ss(this->get_value(key));
                T t; ss >> t;
                return t;
            }

            std::string get_value(const std::string& key) const;
            bool has_value(const std::string& key) const;

        private:
            ConfigStore();
            ~ConfigStore();
            
            struct Data;
            Data* _data;
    };

}
