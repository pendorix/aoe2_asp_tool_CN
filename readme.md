ASP 工具脚本使用手册
    一、简介
        **ASP 工具（asp_tool.py）**是为《帝国时代 II：决定版》场景文件开发的一款命令行工具脚本，用于批量处理触发器和导入 XS 脚本函数。它支持以下功能：

            导入外部 XS 常量与函数 --模式 importxs
            删除部分或全部触发器 -- 模式 del
            从一个场景迁移触发器到另一个场景 -- 模式 mig
            重新排列触发器顺序（可选随机打乱） -- 模式 reorder
            
        ※本工具基于 AoE2ScenarioParser 实现。

    二、使用前准备
        安装依赖：
            pip install AoE2ScenarioParser

        设置 Python 脚本可执行权限（Linux/macOS）：
            chmod +x asp_tool.py

        ※推荐使用 Python 3.8 及以上。

    三、命令格式
        python asp_tool.py -m [模式] -i [配置文件路径]
        参数说明：
            参数	说明
            -m	指定操作模式：reorder（重排触发器）、del（删除触发器）、mig（迁移触发器）
            -i	JSON 格式的配置文件路径

    四、功能说明与示例配置
        1. 模式：reorder（触发器重排）
            功能：
                按触发器“显示顺序”重新排序，也可选打乱顺序。

            示例配置 JSON：
                {
                    "scx_path": "path/to/your_map.aoe2scenario",
                    "output_path": "path/to/output_map.aoe2scenario",
                    "shuffle_order": false,
                    "show_order": true
                }

            调用示例：
                python asp_tool.py -m reorder -i reorder_config.json


        2. 模式：del（删除触发器）
            功能：
                删除场景中指定区间的触发器，可实现清空触发器功能。

            示例配置 JSON：
                {
                    "src_path": "path/to/input_map.aoe2scenario",
                    "des_path": "path/to/output_map.aoe2scenario",
                    "del_range": [0, -1]
                }
                del_range 含义为 [起始索引, 结束索引]，-1 表示末尾。

            调用示例：
                python asp_tool.py -m del -i del_config.json

        3. 模式：mig（迁移触发器）
            功能：
                将某个场景的触发器迁移到另一个场景。

            示例配置 JSON：
                {
                    "scn1_path": "path/to/source_map.aoe2scenario",
                    "scn2_path": "path/to/target_map.aoe2scenario",
                    "output_path": "path/to/final_output.aoe2scenario",
                    "migrate_triggers": ["触发器1", "触发器2"],
                    "insert_pos": -1
                }
                insert_pos 表示插入位置，-1 代表追加到末尾。

            调用示例：
                python asp_tool.py -m mig -i mig_config.json

        4. 模式：importxs（xs脚本导入）
            功能： 
                将多个 XS 脚本文件导入到指定场景文件，并设置相关参数。

            示例配置 JSON：
                {
                    "src_path": "./inputs/scenario/test_from.aoe2scenario",
                    "des_path": "./inputs/scenario/test_to.aoe2scenario",
                    "scx_title": "地图标题",
                    "script_title": "XS Functions",
                    "xs_files": [
                        "./inputs/scenario/const.xs",
                        "./inputs/scenario/unitConst.xs"
                    ]
                }

    五、JSON 文件中的参数含义
        对于 params.json 文件中的输入信息，它们用于指定各个模式 (reorder, del, mig) 运行时的参数配置。以下是具体的含义和注意事项：

        1. reorder 模式：
            {
                "scx_path": "./test_from.aoe2scenario",
                "output_path": "./test_to.aoe2scenario",
                "shuffle_order": true,
                "show_order": true
            }
            scx_path: 需要重排触发器的 AOE2 场景文件路径
            output_path: 处理后的新场景文件路径
            shuffle_order: 是否随机打乱触发器顺序 (true / false)
            show_order: 是否显示触发器顺序 (true / false)

        2. del 模式：
            {
                "src_path": "./test_from.aoe2scenario",
                "des_path": "./test_to.aoe2scenario",
                "del_range": [0, 1]
            }
            src_path: 原始场景文件路径
            des_path: 删除触发器后的新场景文件路径
            del_range: 需要删除的触发器索引范围，[起始索引, 结束索引]

        3. mig 模式：
            {
                "scn1_path": "./test_from.aoe2scenario",
                "scn2_path": "./test_to.aoe2scenario",
                "migrate_triggers": ["XS函数定义", "T5"],
                "insert_pos": -1,
                "output_path": "./test_del_reorder.aoe2scenario"
            }
            scn1_path: 触发器迁移的源场景文件
            scn2_path: 触发器迁移的目标场景文件
            migrate_triggers: 需要迁移的触发器名称列表
            insert_pos: 插入位置，-1 表示末尾
            output_path: 迁移后生成的新场景文件路径

        4. importxs 模式：
            {
                "src_path": "./inputs/scenario/input_map.aoe2scenario",
                "des_path": "./inputs/scenario/output_map.aoe2scenario",
                "scx_title": "地图标题",
                "script_title": "XS Functions",
                "xs_files": ["const.xs", "base_func.xs", "user_func.xs"]
            }
            src_path: 需要导入 XS 脚本的原始 AOE2 场景文件路径
            des_path: 处理后生成的新场景文件路径
            scx_title: 场景的标题，通常用于标识地图
            script_title: XS 触发器的标题，一般用于定义脚本逻辑
            xs_files: 需要导入的 XS 脚本文件列表

        ※注意事项
            确保路径正确
                scx_path, output_path, src_path 等所有路径必须有效。
                可使用 绝对路径 或 相对路径，避免路径错误。

            数组格式要正确
                del_range 需要以 [起始索引, 结束索引] 的数组格式填写。
                migrate_triggers 必须是触发器名称的 字符串数组，例如 ["XS函数定义", "T5"]。

            布尔值必须是 true / false
                JSON 中布尔值不能写 True 或 False（Python格式），必须用 true / false。

            insert_pos 的用法
                -1 表示在目标场景的最后插入迁移的触发器。
                可以使用具体索引，例如 2 表示在 索引 2 位置 插入。

            JSON 文件编码
                建议保存为 UTF-8 编码格式，避免中文字符显示错误。

            如何指定 JSON 文件
                运行命令时指定：
                    python asp_tool.py -m mig -i params.json
                这样脚本会自动从 params.json 读取 mig 模式的参数。

    六、日志系统
        所有运行日志会保存在当前目录的 asp_tools_log/ 文件夹下，自动按时间命名。
        日志中包括函数名、行号、触发器信息、异常信息，便于排查错误。

    七、注意事项
        请勿使用 UTF-8 BOM 格式保存 JSON 或 XS 文件。
        文件路径尽量避免中文及特殊字符。
        请在使用 importxs 模式前确认 .xs 脚本格式规范，尤其是分隔符。
        若在 ARM 架构设备（如 Apple Silicon）使用，请确保 ld-linux-aarch64.so.2 支持。

    八、版本信息
        版本：1.0
        作者：traffic
        邮箱：shikoushou41@gmail.com
        日期：2025-06-01
        授权协议：MIT License