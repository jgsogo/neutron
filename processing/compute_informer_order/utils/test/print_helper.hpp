

namespace boost {
    namespace test_tools {
        namespace tt_detail {

            template <typename... Args>
            struct print_log_value<std::tuple<Args...> >
            {
                void operator()(std::ostream& os, const typename std::tuple<Args...>& pr)
                {
                    os << pr;
                }
            };

        }
    }
}
