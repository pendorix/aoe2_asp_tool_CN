# /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: asp_tool.py
@brief: 帝国时代2决定版场景处理工具脚本
@version: 1.0
@author: traffic
@contact: shikoushou41@gmail.com
@date: 2025-06-01
@license: MIT License
@description:
    该脚本提供了一些帝国时代2决定版场景处理的工具函数，包括：
    - 加载外部 XS 脚本常量
    - 导入 XS 脚本到场景
    - 删除触发器
    - 迁移触发器
    - 重排触发器
@note:
    1. 需要安装 AoE2ScenarioParser 库。
    2. 使用前请确保已正确配置环境。
    3. 如果是macOS或Linux用户，请确保脚本有执行权限。本脚本有调用xs-check的情况，
       请保证你的计算机物理平台支持 ld-linux-aarch64.so.2 
@usage:
    python asp_tool.py -m reorder
"""
import argparse
import sys
import os
import re
import json
import logging
from datetime import datetime
import random
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

# ============================================
# 帝国时代工具函数区
# ============================================

def load_const(path: str):
    '''
    函数名：外部xs脚本常量加载处理
    功能：从指定路径加载外部 XS 文件中的常量字符串。
    参数：
        path - 外部 XS 文件的路径。
    返回：
        返回字符串内容（即 XS 文件中的所有文本）。
    异常处理：
        如果文件无法读取，将抛出异常。
    '''
    try:
        with open(path, mode='r', encoding='utf-8') as fp:
            consts = fp.read()
        return consts
    except Exception as e:
        logging.error(f"[错误] 加载常量文件失败：{e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

def load_function(path: str, sep: str = '\n\n\n'):
    '''
    函数名：load_function
    功能：从外部 XS 文件中读取多个函数并返回其列表。
    参数：
        path - XS 脚本路径
        sep - 拆分函数体的分隔符（默认：三个换行）
    返回：
        (fn_list, fn_list_clean) - 原始函数块列表及去除注释和空格的函数块列表
    异常处理：
        如果文件无法读取或格式错误，将抛出异常。
    '''
    try:
        with open(path, mode='r', encoding='utf-8') as fp:
            context = fp.read()
        fn_list = context.split(sep)
        fn_list_clean = []
        for fn in fn_list:
            if not fn or fn.strip() == '':
                continue
            # 去除文档注释、多行注释、单行注释
            res = re.sub(r'/\*\*(.*?)\*/', '', fn, flags=re.S)
            res = re.sub(r'/\*(.*?)\*/', '', res, flags=re.S)
            res = re.sub('//.*', '', res)
            res = res.replace('    ', '').replace(' || ', '||').replace('\t', '').replace(', ', ',').replace('\n', '')
            if res.strip():
                fn_list_clean.append(res)
        return fn_list, fn_list_clean
    except Exception as e:
        logging.error(f"[错误] 加载函数失败：{e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

def Dict2Json(obj, path, mode='w+', encoding='utf-8', ensure_ascii=True):
    '''
    函数名：Dict2Json
    功能：将字典对象保存为 JSON 文件。
    参数：
        obj - 字典或类似字典的对象
        path - 保存路径
        mode - 文件打开模式（默认 w+）
        encoding - 编码方式（默认 utf-8）
        ensure_ascii - 是否保证输出 ASCII（为 True 可防乱码）
    返回：
        无
    异常处理：
        如果写入失败则抛出异常。
    '''
    try:
        with open(path, mode=mode, encoding=encoding) as fp:
            json.dump(obj, fp, ensure_ascii=ensure_ascii)
    except Exception as e:
        logging.error(f"[错误] 写入 JSON 失败：{e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

def import_xs(scx_infos: dict, sep: str='\n\n\n'):
    '''
    函数名：import_xs
    功能：将外部 XS 脚本导入到指定的 AoE2 决定版场景中。
    参数：
        scx_infos - 包含路径与文件的字典信息
        sep - 函数体分隔符，默认使用三个换行
    返回：
        成功返回 True，失败返回 False
    '''
    try:
        SRC_PATH = scx_infos.get('src_path')
        if not SRC_PATH or SRC_PATH.strip() == '':
            logging.info("[错误] 未提供有效的源路径。")
            return False

        scenario = AoE2DEScenario.from_file(SRC_PATH)
        trigger_mgr = scenario.trigger_manager

        SCX_TITLE = scx_infos.get('scx_title')
        if SCX_TITLE and SCX_TITLE.strip():
            title_trigger = trigger_mgr.add_trigger(str(SCX_TITLE), enabled=False)
            logging.info(f"设置地图标题： {title_trigger.name}")

        XS_FUNC_TITLE = scx_infos.get('script_title') or 'XS Functions'
        if len(scx_infos['xs_files']) >= 1:
            fn_trigger = trigger_mgr.add_trigger(XS_FUNC_TITLE, enabled=False)
            XS_CONST = scx_infos['xs_files'][0]
            fn_trigger.new_condition.script_call(load_const(XS_CONST))
            logging.info("导入 XS 常量成功。")

            if len(scx_infos['xs_files']) >= 2:
                BASE_FN = scx_infos['xs_files'][1]
                _, fn_list = load_function(BASE_FN, sep=sep)
                for fn in fn_list:
                    fn_trigger.new_condition.script_call(fn)
                logging.info("导入基础函数成功。")

                if len(scx_infos['xs_files']) >= 3:
                    UDF_FN = scx_infos['xs_files'][2]
                    _, udf_list = load_function(UDF_FN, sep=sep)
                    for trigger in trigger_mgr.triggers:
                        if trigger.name == XS_FUNC_TITLE:
                            for udf in udf_list:
                                trigger.new_condition.script_call(udf)
                    logging.info("导入用户自定义函数成功。")
        else:
            logging.info("[错误] 未提供 XS 脚本文件。")
            return False

        DES_PATH = scx_infos['des_path']
        scenario.write_to_file(DES_PATH)
        logging.info(f"最终保存路径： {DES_PATH}")
        return True
    except Exception as e:
        logging.error(f"[错误] 导入 XS 过程失败：{e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

def _del_range(si, ei, trigger_counts):
    """
    计算要删除的触发器范围。

    参数:
        si: 起始索引
        ei: 结束索引
        trigger_counts: 触发器总数

    返回:
        经过调整后的起始索引和结束索引
    """
    if si < 0:
        si = 0
    elif si >= trigger_counts:
        si = trigger_counts - 1

    if ei == -1 or ei > trigger_counts:
        ei = trigger_counts
    elif ei == 0:
        ei += 1

    if si > ei:
        si, ei = ei, si

    return si, ei

def del_triggers(scx_infos: dict):
    """
    删除部分或全部触发器。

    参数:
        scx_infos: 包含玩家信息和场景信息的字典。

    返回:
        如果成功删除触发器，则返回 True；否则返回 False。
    """
    # 从 src_path 加载场景文件
    SRC_PATH = scx_infos.get('src_path', None)
    if SRC_PATH in {None, '', ' ', '\n', '\t'}:
        logging.info(f"源场景路径不存在。 {SRC_PATH}")
        return False

    DES_PATH = scx_infos.get('des_path', None)
    if DES_PATH in {None, '', ' ', '\n', '\t'}:
        logging.info(f"目标场景路径不存在。 {DES_PATH}")
        return False

    scenario = AoE2DEScenario.from_file(SRC_PATH)

    # 复制所有触发器
    trigger_mgr = scenario.trigger_manager
    copy_triggers = trigger_mgr.triggers
    trigger_counts = len(copy_triggers)
    logging.info(f"场景中的触发器数量:  {trigger_counts}")

    # 获取删除范围
    start_idx, end_idx = _del_range(scx_infos['del_range'][0], scx_infos['del_range'][1], trigger_counts)

    if start_idx == 0 and end_idx == trigger_counts:
        logging.info("删除所有触发器。")
        # 删除所有触发器，将 trigger_manager.triggers 设为空列表
        trigger_mgr.triggers = []
        scenario.write_to_file(DES_PATH)
        logging.info("成功删除所有触发器。")
    else:
        logging.info(f"删除触发器范围: ({start_idx}, {end_idx})。")    
        # 删除指定范围的触发器: [start_idx, end_idx)
        trigger_mgr.triggers = copy_triggers[0:start_idx] + copy_triggers[end_idx: ]
        scenario.write_to_file(DES_PATH)
        logging.info(f"成功删除触发器范围: ({start_idx}, {end_idx})。")
        
    trigger_counts = len(trigger_mgr.triggers)
    logging.info(f"删除后场景中的触发器数量: {trigger_counts}")
    if trigger_counts == 0:
        logging.info("当前场景中没有触发器。")
    return True

def migrate_triggers(scx_infos: dict):
    '''
    将触发器从 `src_map` 迁移到 `des_map`。

    参数:
        scx_infos: 一个包含玩家信息和场景信息的字典。

    返回:
        如果成功迁移触发器，则返回 True；否则返回 False。
    '''
    try:
        # 从文件加载两个场景
        scn1 = AoE2DEScenario.from_file(scx_infos.get('scn1_path', ''))
        scn2 = AoE2DEScenario.from_file(scx_infos.get('scn2_path', ''))

        # 获取两个场景的触发器管理器
        trigger_mgr1 = scn1.trigger_manager
        trigger_mgr2 = scn2.trigger_manager

        # 显示两个地图中的触发器数量
        logging.info(f"地图 1 中的触发器数量: {len(trigger_mgr1.triggers)}")
        logging.info(f"地图 2 中的触发器数量: {len(trigger_mgr2.triggers)}")

        # 遍历 `scn1` 的触发器，筛选出名称在 `scx_infos["migrate_triggers"]` 中的触发器
        migrate_indices = []
        migrate_triggers = []
        for t1 in trigger_mgr1.triggers:
            if t1.name in scx_infos["migrate_triggers"]:
                migrate_indices.append(t1.trigger_id)
                migrate_triggers.append(t1)

        logging.info(f"需要迁移的触发器 ID: {migrate_indices}")

        # 迁移 `migrate_triggers` 列表到 `trigger_mgr2`
        trigger_mgr2.import_triggers(triggers=migrate_triggers, index=scx_infos.get('insert_pos', -1))

        # 按照显示顺序重新排序触发器
        trigger_mgr2.reorder_triggers(trigger_mgr2.trigger_display_order)

        # 保存场景到 `output_path`
        scn2.write_to_file(scx_infos.get('output_path', ''))

        return True
    except Exception as e:
        logging.error(f"迁移触发器时发生错误: {e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

def reorder_scx_triggers(scx_path: str, output_path: str, shuffle_order: bool = False, show_order: bool = True):
    '''
    函数名：reorder_scx_triggers
    功能：根据显示顺序对 AoE2 场景中的触发器进行重排，并可选择是否打乱顺序。
    参数：
        scx_path - 输入场景路径（.aoe2scenario）
        output_path - 输出保存路径（重排后）
        shuffle_order - 是否打乱触发器顺序（默认为 False）
        show_order - 是否打印触发器顺序（显示序与创建序）
    返回：
        无
    '''
    try:
        scenario = AoE2DEScenario.from_file(scx_path)
        trigger_mgr = scenario.trigger_manager
        trigger_amt = len(trigger_mgr.triggers)

        if trigger_amt == 0:
            logging.info("触发器数量为 0，无需重排。")
            return
        elif trigger_amt == 1:
            logging.info("触发器数量为 1，无需重排。")
            return

        # 获取显示顺序与创建顺序
        display_orders = list(range(len(trigger_mgr.trigger_display_order)))
        create_orders = trigger_mgr.trigger_display_order[:]

        if show_order:
            logging.info("显示序\t触发ID\t触发名称")
            logging.info("------------------------------")
            for idx, tid in zip(display_orders, create_orders):
                trigger = trigger_mgr.triggers[tid]
                logging.info(f"{idx}\t\t{tid}\t{trigger.name}")

        if shuffle_order and show_order:
            logging.info("打乱触发器顺序 ......")
            random.shuffle(create_orders)
            logging.info("显示序\t触发ID\t触发名称")
            logging.info("------------------------------")
            for idx, tid in zip(display_orders, create_orders):
                trigger = trigger_mgr.triggers[tid]
                logging.info(f"{idx}\t\t{tid}\t{trigger.name}")
            logging.info("触发器顺序已打乱。")

        elif shuffle_order and not show_order:
            logging.info("打乱触发器顺序 ......")
            random.shuffle(create_orders)
            logging.info("触发器顺序已打乱。")
                
        if display_orders == create_orders and not shuffle_order:
            logging.info("触发器顺序未打乱，无需重排。")
            return

        logging.info("开始重新排列触发器 ......")
        trigger_mgr.reorder_triggers(create_orders)
        scenario.write_to_file(output_path)
        logging.info("触发器重新排列完成！")

    except Exception as e:
        logging.error(f"[错误] 触发器重新排列失败：{e}", exc_info=True)
        sys.exit(1)  # 退出程序，返回错误状态码

# ============================================
# 通用函数区
# ============================================

def init_logging(log_dir: str = "asp_tools_log"):
    '''
    函数名：init_logging  
    功能：初始化日志系统，创建日志目录，配置日志输出到文件和控制台，并附带函数名与行号信息。
    参数：
        log_dir - 保存日志文件的目录，默认为 "asp_tools_log"
    返回：
        无
    异常处理：
        初始化失败时在终端输出详细异常信息。
    '''
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"asp_tools-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.log")
        
        # 日志格式中加入函数名（funcName）与行号（lineno）
        log_format = '%(asctime)s - %(levelname)s - %(funcName)s : %(lineno)d - %(message)s'
        
        # 文件日志处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format))

        # 控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))

        # 设置主日志系统
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler]
        )

        logging.info("日志系统初始化完成。")

    except Exception as e:
        logging.error(f"日志系统初始化失败：{e}", flush=True)
        import traceback
        traceback.logging.info_exc()
        sys.exit(1)  # 退出程序，返回错误状态码

# ============================================
# 主函数区
# ============================================
        
def main():
    '''
    函数名：main
    功能：脚本入口函数，初始化日志并执行示例操作，同时记录处理时间。
    返回：
        无
    '''
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="ASP 工具脚本")
    parser.add_argument(
        "-m",
        choices=["reorder", "del", "mig", "importxs"],
        required=True,
        help="操作模式，必须是 'reorder'、'del'、'mig' 或 'importxs'"
    )
    parser.add_argument("-i", type=str, required=True, help="参数 JSON 文件的路径")
    
    args = parser.parse_args()

    # 初始化日志
    init_logging()
    logging.info("ASP 工具脚本启动。")

    # 记录开始时刻
    start_time = datetime.now()
    logging.info(f"任务开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 读取 JSON 文件
    try:
        with open(args.i, "r", encoding="utf-8") as file:
            params = json.load(file)
    except Exception as e:
        logging.error(f"无法读取 JSON 文件: {e}", exc_info=True)
        sys.exit(1)

    # 根据参数执行不同的操作
    mode_params = params.get(args.m)
    if not mode_params:
        logging.error(f"模式 '{args.m}' 在 JSON 文件中未定义。 {args.i}")
        sys.exit(1)

    if args.m.lower() == "reorder":
        logging.info("执行重排触发器操作。")
        reorder_scx_triggers(**mode_params)

    elif args.m.lower() == "del":
        logging.info("执行 DEL 操作。")
        del_triggers(mode_params)

    elif args.m.lower() == "mig":
        logging.info("执行 MIG 操作。")
        migrate_triggers(mode_params)

    elif args.m.lower() == "importxs":
        logging.info("执行 Import XS 操作。")
        import_xs(mode_params)

    # 记录结束时刻
    end_time = datetime.now()
    logging.info(f"任务结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 计算处理时间
    elapsed_time = end_time - start_time
    logging.info(f"任务总处理时间: {elapsed_time.total_seconds():.2f} 秒")
    logging.info("操作完成。")
    
if __name__ == "__main__":
    main()