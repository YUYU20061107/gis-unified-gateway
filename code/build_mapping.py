# -*- coding: utf-8 -*-
"""build_mapping.py — 生成 gateway-v02 的全部注册表与映射文件。

产物（同目录）：
  mapping.json             基础 8 动词 × 8 后端映射（沿 v0.1 口径扩展至
                           postgis/geoserver/istsos）＋object_model_v02 段
  verbs.json               第一波 40 动词（设计 §2 V01–V40）规格：分级、
                           confirm 策略、逐后端映射（轮子名/状态/注记）
  gp_registry.json         ArcGIS GP 注册表：由 help-survey/arcgis.md 表格
                           解析（1833 条判断、白名单第一批 243、defer 152、
                           破坏类通道拦截名单、许可三字段种子位）
  processing_registry.json QGIS Processing 种子账：由 help-survey/qgis.md
                           解析（374 条，状态一律 seed；defer＋§3.1 点名
                           构成硬拦截名单）
  postgis_templates.json   PostGIS 参数化 SQL 模板集（设计 §3.3：永不裸
                           SQL；值走绑定参数，标识符过白名单正则）
  mock_tools.json          自检 mock 后端应提供的原生工具名清单（由上面
                           全部映射汇出，保证 mock 面与映射面一致）

校验纪律（沿 v0.1）：映射点名的原生工具必须真实存在于合集 manifest
（catalog 直读 catalog_server.py 的 TOOLS）；普查计数对不上（1833 /
803/878/152 / 243 / 374 / 82/242/50）直接报错退出，不许静默凑数。
设计标「待验/未核实」的映射在本文件里 status=unverified，网关拒绝执行
并回 UNVERIFIED_MAPPING——登记在册，但绝不写成可用。
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
MANIFEST = os.environ.get("GIS_GATEWAY_MANIFEST") or os.path.expanduser(
    "~/workspace/dsh-skills/gis-agent-bridges/manifest/tools-manifest.json")
SURVEY_ARCGIS = os.path.join(ROOT, "help-survey", "arcgis.md")
SURVEY_QGIS = os.path.join(ROOT, "help-survey", "qgis.md")
CATALOG_DIR = os.path.join(ROOT, "data-catalog")
CATALOG_SERVER = os.path.join(CATALOG_DIR, "catalog_server.py")
CATALOG_INDEX = os.path.join(CATALOG_DIR, "catalog.json")

BACKENDS = ["supermap", "arcgis-pro", "arcmap", "qgis",
            "catalog", "postgis", "geoserver", "istsos", "gdal",
            "qgis-cli", "iserver"]
PKG = {"supermap": "supermap", "arcgis-pro": "arcgis-pro",
       "arcmap": "arcmap", "qgis": "qgis", "postgis": "postgis",
       "geoserver": "geoserver", "istsos": "istsos", "gdal": "gdal",
       "qgis-cli": "qgis-cli", "iserver": "iserver"}

# GDAL 后端首版工具面（code/gdal_server.py）。它不经 gis-agent-bridges
# manifest，而是网关自带的本地 CLI 适配层；native 名校验以本集合为准。
GDAL_TOOLS = {"gdal_ping", "gdal_discover", "gdal_reproject",
              "gdal_convert_format", "gdal_clip", "gdal_slope",
              "gdal_aspect", "gdal_hillshade"}

# QGIS 无头 Processing CLI 后端（与 in-app qgis 桥分开）：只做
# qgis_process 执行，不冒充打开工程/图层视图。
QGIS_CLI_TOOLS = {"qgis_ping", "qgis_discover", "qgis_run_processing"}

# iServer 只读演示后端（demo-instance-verified）：只登记已由 GET 探针确认的
# 服务目录与 map-china REST 面；data/spatial REST 在演示实例 502，不登记。
ISERVER_TOOLS = {"iserver_ping", "iserver_discover", "iserver_project_info",
                 "iserver_list_maps", "iserver_list_layers",
                 "iserver_list_datasets", "iserver_list_services"}


def fail(msg):
    print("FAIL: %s" % msg, file=sys.stderr)
    sys.exit(1)


# =====================================================================
# 第一部分：基础 8 动词映射（v0.1 TABLE 扩展至 8 后端）
# =====================================================================
# 每项 (原生工具列表, 参数映射说明) 或 None（该后端无此能力）。

TABLE = {
    "gis_ping": {
        "semantics": "桥是否在线",
        "backends": {
            "supermap": (["supermap_ping"], "无参数"),
            "arcgis-pro": (["arcgis_ping"], "无参数"),
            "arcmap": (["arcmap_ping"], "无参数"),
            "qgis": (["qgis_ping"], "无参数"),
            "catalog": None,
            "postgis": (["postgis_ping"], "无参数"),
            "geoserver": (["geoserver_ping"], "无参数"),
            "istsos": (["istsos_ping"], "无参数"),
        },
    },
    "gis_discover": {
        "semantics": "发现接入方式 + 能力协商；网关在原生 discover 结果外再叠加统一 envelope（v0.2 另加治理节，见 gateway.py）",
        "backends": {
            "supermap": (["supermap_discover"], "无参数"),
            "arcgis-pro": (["arcgis_discover"], "无参数"),
            "arcmap": (["arcmap_discover"], "无参数"),
            "qgis": (["qgis_discover"], "无参数"),
            "catalog": (["gis_catalog_list"],
                        "目录后端无原生 discover：所有后端的 gis_discover 都由网关实时调 gis_catalog_list 聚合 counts，生成 data_catalog 一节"),
            "postgis": (["postgis_discover"], "无参数；discover 以 PostGIS_Full_Version 为版本证据（设计 §3.3，桥侧回包为准）"),
            "geoserver": (["geoserver_discover"], "无参数"),
            "istsos": (["istsos_discover"], "无参数"),
        },
    },
    "gis_project_info": {
        "semantics": "工程概览；kind 按后端区分（workspace/project/document/catalog/database/service），不强行改名",
        "backends": {
            "supermap": (["supermap_workspace_info"], "无参数；kind=workspace"),
            "arcgis-pro": (["arcgis_project_info"], "无参数；kind=project"),
            "arcmap": (["arcmap_document_info"], "无参数；kind=document"),
            "qgis": (["qgis_project_info"], "无参数；kind=project"),
            "catalog": ([], "网关本地合成 project{kind:catalog}，不调原生"),
            "postgis": (["postgis_list_spatial_tables"],
                        "数据库无工程概念：以空间表清单作概览，网关回包标 kind=database"),
            "geoserver": (["geoserver_list_workspaces"],
                          "服务无工程概念：以工作区清单作概览，网关回包标 kind=service"),
            "istsos": (["istsos_discover"],
                       "STA 服务根信息即 discover 结果，网关复用并标 kind=service"),
        },
    },
    "gis_list_maps": {
        "semantics": "列地图",
        "backends": {
            "supermap": (["supermap_list_maps"], "无参数"),
            "arcgis-pro": (["arcgis_list_maps"], "无参数"),
            "arcmap": (["arcmap_list_dataframes"],
                       "ArcMap 无地图概念：改调数据框列表，回包 maps 每项标注 type=dataframe、顶层 maps_kind=dataframe"),
            "qgis": None,  # 网关本地返回空列表 + note=qgis_has_no_maps
            "catalog": None,
            "postgis": None,  # 数据库无地图概念
            "geoserver": None,  # 服务端无地图概念（图层走 gis_list_layers）
            "istsos": None,
        },
    },
    "gis_list_layers": {
        "semantics": "列图层（下标、名称、显隐；source/broken 后端有才有，无则留空不编造）",
        "backends": {
            "supermap": (["supermap_list_layers"], "统一 map -> 原生 map（可选）"),
            "arcgis-pro": (["arcgis_list_layers"], "统一 map -> 原生 map（可选）"),
            "arcmap": (["arcmap_list_layers"], "统一 map -> 原生 dataframe（可选）"),
            "qgis": (["qgis_list_layers"], "QGIS 图层是工程级的，无 map 参数；传了 map 会被忽略并回包附注"),
            "catalog": None,
            "postgis": None,  # 表不是图层：空间表走 gis_list_datasets
            "geoserver": (["geoserver_list_layers"], "统一 workspace -> 原生 workspace（可选，前缀过滤）"),
            "istsos": None,  # STA 实体不是图层：走 gis_query_observations / gis_list_services
        },
    },
    "gis_list_datasets": {
        "semantics": "列数据集（核心对象 dataset）：supermap=厂商工作空间数据源/数据集；catalog=平台目录登记数据集；postgis=数据库空间表；其余后端无此概念 NOT_SUPPORTED",
        "backends": {
            "supermap": (["supermap_list_datasources", "supermap_list_datasets"],
                         "两次原生调用合并回包：{datasources, datasets}；统一 datasource -> 原生 datasource（可选）"),
            "arcgis-pro": None,
            "arcmap": None,
            "qgis": None,
            "catalog": (["gis_catalog_list"],
                        "平台数据目录的登记数据集：回核心对象 dataset（每项加 object=dataset、stac_role=collection 标记），统一 type / commercial_use -> 原生同名过滤参数"),
            "postgis": (["postgis_list_spatial_tables"],
                        "数据库空间表即服务端 dataset：回包带 source_kind=server_database，与厂商工作空间/平台目录显式区分"),
            "geoserver": None,  # store 不经桥暴露，图层走 gis_list_layers
            "istsos": None,
        },
    },
    "gis_set_layer_visible": {
        "semantics": "视图级设图层显隐，只改显示状态、可逆",
        "backends": {
            "supermap": (["supermap_set_layer_visible"], "map（可选）/ layer / visible 同名透传"),
            "arcgis-pro": (["arcgis_set_layer_visible"], "map（可选）/ layer / visible 同名透传"),
            "arcmap": (["arcmap_set_layer_visible"], "统一 map -> 原生 dataframe（可选）；layer / visible 同名透传"),
            "qgis": (["qgis_set_layer_visible"], "layer / visible 同名透传，无 map"),
            "catalog": None,
            "postgis": None,
            "geoserver": None,  # 图层显隐是客户端视图概念，服务端无此面
            "istsos": None,
        },
    },
    "gis_zoom_to_layer": {
        "semantics": "视图级缩放到目标范围；统一参数 target={type: layer|dataset, id}，网关按后端翻译，翻译不了返回 NOT_SUPPORTED，不猜测",
        "backends": {
            "supermap": (["supermap_zoom_to_dataset"],
                         "仅 target.type=dataset 可翻译：dataset<-target.id，datasource/map 可选透传；type=layer 返回 NOT_SUPPORTED"),
            "arcgis-pro": (["arcgis_zoom_to_layer"],
                           "仅 target.type=layer：layer<-target.id，map 可选透传；type=dataset 返回 NOT_SUPPORTED"),
            "arcmap": (["arcmap_zoom_to_layer"],
                       "仅 target.type=layer：layer<-target.id，统一 map -> 原生 dataframe；type=dataset 返回 NOT_SUPPORTED"),
            "qgis": (["qgis_zoom_to_layer"],
                     "仅 target.type=layer：layer<-target.id；type=dataset 返回 NOT_SUPPORTED"),
            "catalog": None,
            "postgis": None,
            "geoserver": None,
            "istsos": None,
        },
    },
}

BASE_VERBS = list(TABLE.keys())

# v0.3 GDAL 后端：基础 8 动词只开放 ping/discover。文件后端没有工程、地图、
# 图层、数据集的产品概念；这些基础动词如实 NULL（网关回 NOT_SUPPORTED），
# 不用目录/文件列表冒充。
TABLE["gis_ping"]["backends"]["gdal"] = (["gdal_ping"], "无参数")
TABLE["gis_discover"]["backends"]["gdal"] = (
    ["gdal_discover"], "本地 GDAL 版本 / 驱动计数 / 工具面")
TABLE["gis_ping"]["backends"]["qgis-cli"] = (["qgis_ping"], "无参数")
TABLE["gis_discover"]["backends"]["qgis-cli"] = (
    ["qgis_discover"], "qgis_process CLI 版本 / 模式")
TABLE["gis_ping"]["backends"]["iserver"] = (["iserver_ping"], "GET services.json")
TABLE["gis_discover"]["backends"]["iserver"] = (
    ["iserver_discover"], "GET services.json 服务目录摘要")
TABLE["gis_project_info"]["backends"]["iserver"] = (
    ["iserver_project_info"], "服务目录概览，kind=service")
TABLE["gis_list_maps"]["backends"]["iserver"] = (
    ["iserver_list_maps"], "默认 GET map-china/rest/maps.json")
TABLE["gis_list_layers"]["backends"]["iserver"] = (
    ["iserver_list_layers"],
    "统一 map -> 地图名；默认 map-china/China；GET layers.json")
TABLE["gis_list_datasets"]["backends"]["iserver"] = (
    ["iserver_list_datasets"],
    "默认 data-china/China；GET datasources + datasets.json")
for _v in ("gis_project_info", "gis_list_maps", "gis_list_layers",
           "gis_list_datasets", "gis_set_layer_visible",
           "gis_zoom_to_layer"):
    TABLE[_v]["backends"]["gdal"] = None
    TABLE[_v]["backends"]["qgis-cli"] = None
for _v in ("gis_set_layer_visible", "gis_zoom_to_layer"):
    TABLE[_v]["backends"]["iserver"] = None


BACKEND_META = {
    "supermap": {
        "project_kind": "workspace",
        "extension_namespaces": ["gis.supermap.*"],
        "extension_note": "v0.2：第一波 40 动词中 SuperMap 侧映射见 gis_discover 的 v02_verbs 节；待验映射登记但拒绝执行（UNVERIFIED_MAPPING）",
    },
    "arcgis-pro": {
        "project_kind": "project",
        "extension_namespaces": ["gis.arcgis.*"],
        "extension_note": "v0.2：GP 直调通道（gis_run_gp）只开白名单第一批（三箱 core 子集扣破坏类）；defer 硬拦截；许可/扩展/弃用三字段见 discover 的 gp_governance 节（种子位，未补齐前为 null）",
    },
    "arcmap": {
        "project_kind": "document",
        "extension_namespaces": ["gis.arcgis.*"],
        "extension_note": "ArcMap 线冻结存量（决策 D3）：只保留基础 8 动词，不开 GP 通道、不新增第一波动词映射；桥内既有出图工具 arcmap_export_map_image 不升统一面",
    },
    "qgis": {
        "project_kind": "project",
        "extension_namespaces": ["gis.qgis.*"],
        "extension_note": "v0.2：Processing 执行面经种子注册表治理（374 条 seed，实机枚举为真源，D6）；defer 与 executesql/原地覆写类硬拦截",
    },
    "catalog": {
        "project_kind": "catalog",
        "extension_namespaces": [],
        "extension_note": "平台数据目录：基础动词只开放 discover / project_info / list_datasets 三件；另作 V34/V39 的许可闸数据源（gis_catalog_describe），不直接进统一工具面",
    },
    "postgis": {
        "project_kind": "database",
        "extension_namespaces": ["gis.postgis.*"],
        "extension_note": "v0.2 新增服务端后端：统一动词落为参数化 SQL 模板（postgis_templates.json），永不裸 SQL；v0.3 Phase 4B 在隔离本地 PostgreSQL 16.15/PostGIS 3.6 实测 38/38 模板 + 网关 21/21；生产 DSN 未配置",
    },
    "geoserver": {
        "project_kind": "service",
        "extension_namespaces": ["gis.geoserver.*"],
        "extension_note": "v0.2 新增服务端后端：只读目录面经既有桥工具；发布（gis_publish_layer）走 REST 发布链，桥侧发布工具待实现（pending），网关先行翻译与许可闸",
    },
    "istsos": {
        "project_kind": "service",
        "extension_namespaces": ["gis.istsos.*"],
        "extension_note": "v0.2 新增服务端后端：STA 实体读补全 8/8——Things/Datastreams/Observations 经既有桥工具，其余 5 实体经桥侧通用实体查询（pending）；写面本波不开",
    },
    "gdal": {
        "project_kind": "file",
        "extension_namespaces": ["gis.gdal.*"],
        "extension_note": "v0.3 新增本地 GDAL 后端首版：ping/discover + 格式转换/重投影/裁剪（矢量+栅格）+ 坡度/坡向/山体阴影；每条 ok 映射均由本地 GDAL 3.13.3 CLI 实跑；写操作只写新 target，target 已存在拒绝覆盖",
    },
    "qgis-cli": {
        "project_kind": "processing",
        "extension_namespaces": ["gis.qgis.*"],
        "extension_note": "v0.3 新增 QGIS 无头 Processing 后端：qgis_process CLI，只开 V02 执行面与 V03/V04 注册表；不提供打开工程/图层视图能力（那是 in-app qgis 桥的面，二者分开）",
    },
    "iserver": {
        "project_kind": "service",
        "extension_namespaces": ["gis.iserver.*"],
        "extension_note": "v0.3 Phase 3：官方公开演示实例（demo-instance-verified，非本机、版本未确认）；仅 GET；服务目录 115、map-china 4 地图/China 13 子层、data-china 47 数据集、spatialanalyst 根/子资源形状已探针确认；空间分析执行未尝试（仅 GET）；不冒充本机校准",
    },
}

OBJECT_MODEL_V02 = {
    "version": "0.2",
    "basis": "UPGRADE-DESIGN-V02.md §1.14/§3.4 + gateway-v01/OBJECT-MODEL-V01.md",
    "changes_vs_v01": [
        "服务端对象借 GeoServer 分工：workspace / store / layer / style（不另发明），随 postgis/geoserver/istsos 三后端进网关",
        "catalog 记录新增发布一节（publication）的结构扩展位：发布成功后回写 {service_backend, layer, endpoints, published_at}；catalog_server 尚无回写工具，v0.2 网关回包先带 writeback.status=pending_catalog_support，不假装已回写（见 OBJECT-MODEL-V02.md）",
        "gis_serve_vector_tile 的回包为二进制句柄形态 {content_type, bytes|tile_ref}，不进 JSON 文本面",
        "dataset 的来源再添一类：source_kind=server_database（backend=postgis 的空间表）",
    ],
    "carried_from_v01": "project{kind} 五形态（+database/service 两形态）、dataset 核心对象、STAC 映射、layer.source=Asset 口径全部沿用 OBJECT-MODEL-V01.md",
}


# =====================================================================
# 第二部分：第一波 40 动词规格（设计 §2 V01–V40）
# =====================================================================
# 映射 status：ok＝按设计落名可执行（桥侧工具 existing 或 pending，pending
# 只表示桥侧执行器待实现，网关翻译与治理已落地）；unverified＝设计标
# 待验/未核实，登记但网关拒绝执行；not_supported＝设计明示不开或后端无
# 此能力面。confirm：required＝网关层必需；bridge＝沿用桥规则（网关透传）；
# none＝只读。R2/R3 的 confirm 由分级强制，不看此字段。

def _ok(kind, **kw):
    d = {"status": "ok", "kind": kind}
    d.update(kw)
    return d


def _unv(kind, note, **kw):
    d = {"status": "unverified", "kind": kind, "note": note}
    d.update(kw)
    return d


def _ns(note):
    return {"status": "not_supported", "note": note}


def _var(arg, variants):
    return {"variant_arg": arg, "variants": variants}


def _nat(name, wheel, existing=False):
    return _ok("native", native=name, wheel=wheel,
               bridge_tool_status="existing" if existing else "pending")


def _gp(func):
    return _ok("gp_named", func=func, wheel=func)


def _proc(alg):
    return _ok("processing", algorithm=alg, wheel=alg)


def _tpl(tid, wheel):
    return _ok("template", template=tid, wheel=wheel)


PENDING_NOTE = "桥侧执行工具待实现（pending）：网关翻译/治理已落地，实机不可用，校准不升格"

VERBS = {
    # ---------------- 通道与注册表组 ----------------
    "gis_run_gp": {
        "vid": "V01", "level": "R1", "confirm": "bridge",
        "semantics": "ArcGIS GP 直调总通道：按 ArcPy 官方命名空间直调地理处理工具；白名单第一批（三箱 core 子集扣破坏类）外硬拦截，defer 回 DEFER_BLOCKED，破坏类回 DESTRUCTIVE_BLOCKED（强制走具名动词）",
        "params": {"backend": "s", "tool": "s", "args": "o", "confirm": "b"},
        "backends": {
            "arcgis-pro": _ok("gp_channel", native="arcgis_run_gp",
                              bridge_tool_status="pending", wheel="arcpy.*"),
            "arcmap": _ns("ArcMap 冻结存量（D3）：不开 GP 通道"),
        },
    },
    "gis_run_processing": {
        "vid": "V02", "level": "R1", "confirm": "required",
        "semantics": "QGIS Processing 执行面：按算法 ID 执行，执行前过种子注册表校验（存在性＋defer 硬拦截）；defer 与 §3.1 点名类（executesql/原地覆写/批量图集）回 DEFER_BLOCKED",
        "params": {"backend": "s", "algorithm": "s", "params": "o", "confirm": "b"},
        "backends": {
            "qgis": _ok("processing_channel", native="qgis_run_processing",
                        bridge_tool_status="existing", wheel="Processing 注册表"),
            "qgis-cli": _ok("processing_channel",
                            native="qgis_run_processing",
                            bridge_tool_status="existing",
                            wheel="qgis_process CLI（无头）"),
        },
    },
    "gis_list_algorithms": {
        "vid": "V03", "level": "R0", "confirm": "none",
        "semantics": "能力注册表枚举：列某后端的算法/工具注册表（ID、提供方、分组、平台判断、映射到的统一动词、状态 seed/verified）",
        "params": {"backend": "s", "provider": "s", "judgment": "s"},
        "backends": {
            "qgis": _ok("registry", registry="processing", wheel="Processing 种子账（普查 374 条）"),
            "qgis-cli": _ok("registry", registry="processing",
                            wheel="Processing 种子账（网关本地，不调 CLI）"),
            "arcgis-pro": _ok("registry", registry="gp", wheel="GP 注册表（普查 1833 条判断）"),
            "postgis": _ok("registry", registry="templates", wheel="PostGIS 模板清单"),
            "supermap": _ok("registry", registry="supermap", wheel="iobjectspy 能力登记表（文件登记，非运行时枚举）"),
        },
    },
    "gis_describe_algorithm": {
        "vid": "V04", "level": "R0", "confirm": "none",
        "semantics": "算法自描述：取单个算法/工具的注册表条目与参数模式说明；种子账无参数模式处如实标 pending，不编造",
        "params": {"backend": "s", "algorithm": "s"},
        "backends": {
            "qgis": _ok("registry", registry="processing", wheel="Processing 种子账条目（参数模式待桥侧 algorithmHelp 建账）"),
            "qgis-cli": _ok("registry", registry="processing",
                            wheel="Processing 种子账条目（网关本地，不调 CLI）"),
            "arcgis-pro": _ok("registry", registry="gp", wheel="GP 注册表条目（签名以 arcpy 实际导入为准）"),
            "postgis": _ok("registry", registry="templates", wheel="PostGIS 模板条目"),
        },
    },
    # ---------------- 数据造改组 ----------------
    "gis_create_dataset": {
        "vid": "V05", "level": "R1", "confirm": "required",
        "semantics": "新建空数据集（矢量/表/栅格容器），指定几何类型与坐标系",
        "params": {"backend": "s", "name": "s", "kind": "s",
                   "geometry_type": "s", "srid": "n", "fields": "a", "confirm": "b"},
        "backends": {
            "arcgis-pro": _var("kind", {
                "vector": _gp("arcpy.management.CreateFeatureClass"),
                "table": _unv("gp_named", "CreateTable 函数名按命名规则生成，待 arcpy 实际导入核对（设计 §2 V05）",
                              func="arcpy.management.CreateTable", wheel="arcpy.management.CreateTable"),
                "raster": _ns("栅格容器创建未在设计 §2 V05 的 Pro 映射内（CreateRasterDataset 未列），本波不开"),
            }),
            "supermap": _nat("supermap_create_dataset", "iobjectspy.data.Datasource.create_dataset"),
            "qgis": _unv("native", "桥侧 PyQGIS 建层未在普查算法清单内、未核实，实现期以桥侧校准为准；不得用 Processing 冒名（设计 §2 V05）",
                         native="qgis_create_layer", wheel="PyQGIS 建层（未核实）"),
            "postgis": _tpl("create_table", "CREATE TABLE + geometry 列（AddGeometryColumn 口径）"),
        },
    },
    "gis_add_field": {
        "vid": "V06", "level": "R2", "confirm": "required",
        "semantics": "给已有数据集加字段（原地改写）",
        "params": {"backend": "s", "dataset": "s", "field": "o", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.AddField"),
            "qgis": _proc("native:addfieldtoattributestable"),
            "supermap": _unv("native", "iobjectspy.data 字段接口具体名在 10.1.0 待验（设计 §2 V06）",
                             native="supermap_add_field", wheel="iobjectspy.data 字段接口（待验）"),
            "postgis": _tpl("add_column", "ALTER TABLE ADD COLUMN"),
        },
    },
    "gis_delete_field": {
        "vid": "V07", "level": "R3", "confirm": "required",
        "semantics": "删字段（破坏性，R3 额外闸：confirm＋target_echo＋影响面预检二次确认）",
        "params": {"backend": "s", "dataset": "s", "fields": "a",
                   "confirm": "b", "target_echo": "s", "preflight_id": "s"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.DeleteField"),
            "qgis": _proc("native:deletecolumn"),
            "supermap": _unv("native", "iobjectspy.data 字段接口具体名在 10.1.0 待验（设计 §2 V07）",
                             native="supermap_delete_field", wheel="iobjectspy.data 字段接口（待验）"),
            "postgis": _tpl("drop_column", "ALTER TABLE DROP COLUMN"),
        },
    },
    "gis_calculate_field": {
        "vid": "V08", "level": "R2", "confirm": "required",
        "semantics": "按表达式计算字段（原地改写，回包标 in_place=true）；表达式语言随后端原生",
        "params": {"backend": "s", "dataset": "s", "field": "s",
                   "expression": "s", "language": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.CalculateField"),
            "qgis": _proc("native:fieldcalculator"),
            "supermap": _unv("native", "iobjectspy.data Recordset 更新具体接口待验（设计 §2 V08）",
                             native="supermap_calculate_field", wheel="iobjectspy.data Recordset 更新（待验）"),
            "postgis": _tpl("update_field", "UPDATE … SET（表达式为受限片段，见模板说明）"),
        },
    },
    "gis_copy_dataset": {
        "vid": "V09", "level": "R1", "confirm": "required",
        "semantics": "同后端内复制数据集为新数据集（跨后端走 gis_convert_format）",
        "params": {"backend": "s", "source": "s", "target": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Copy"),
            "supermap": _nat("supermap_copy_dataset", "iobjectspy.data Dataset 复制"),
            "postgis": _tpl("copy_table", "CREATE TABLE AS SELECT"),
            "qgis": dict(_proc("gdal:convertformat"),
                         note="同库复制为近似映射（经格式转换写出），非原地复制语义"),
        },
    },
    "gis_rename_dataset": {
        "vid": "V10", "level": "R2", "confirm": "required",
        "semantics": "重命名数据集（原地改写）",
        "params": {"backend": "s", "dataset": "s", "new_name": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Rename"),
            "supermap": _nat("supermap_rename_dataset", "iobjectspy.data Dataset 重命名"),
            "postgis": _tpl("rename_table", "ALTER TABLE RENAME"),
            "qgis": _ns("桥侧改名未核实，本波 NOT_SUPPORTED（设计 §2 V10）"),
        },
    },
    "gis_delete_dataset": {
        "vid": "V11", "level": "R3", "confirm": "required",
        "semantics": "删数据集（破坏性，R3 额外闸三件套；只许经本具名动词，总通道内硬拦）",
        "params": {"backend": "s", "dataset": "s", "confirm": "b",
                   "target_echo": "s", "preflight_id": "s"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Delete"),
            "supermap": _nat("supermap_delete_dataset", "iobjectspy.data Dataset 删除"),
            "postgis": _tpl("drop_table", "DROP TABLE"),
            "qgis": _ns("桥侧删除未核实，本波 NOT_SUPPORTED（设计 §2 V11）"),
        },
    },
    "gis_merge_datasets": {
        "vid": "V12", "level": "R1", "confirm": "required",
        "semantics": "多个同构数据集纵向合并为一个新数据集",
        "params": {"backend": "s", "inputs": "a", "target": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Merge"),
            "qgis": _proc("native:mergevectorlayers"),
            "postgis": _tpl("merge_tables", "UNION ALL 建表"),
            "supermap": _unv("native", "iobjectspy.analyst/conversion 合并具体名待验（设计 §2 V12）",
                             native="supermap_merge_datasets", wheel="iobjectspy 合并（待验）"),
        },
    },
    "gis_append_dataset": {
        "vid": "V13", "level": "R2", "confirm": "required",
        "semantics": "把源数据集追加进已存在的目标数据集（原地改写）",
        "params": {"backend": "s", "source": "s", "target": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Append"),
            "postgis": _tpl("insert_select", "INSERT INTO … SELECT"),
            "qgis": _ns("以合并输出替换的近似路径未校准前 NOT_SUPPORTED（设计 §2 V13）"),
            "supermap": _ns("待验，本波 NOT_SUPPORTED（设计 §2 V13）"),
        },
    },
    # ---------------- 坐标系组 ----------------
    "gis_assign_projection": {
        "vid": "V14", "level": "R2", "confirm": "required",
        "semantics": "只定义/覆写坐标系元数据，不动坐标值（与 gis_reproject 严格区分，回包标 metadata_only=true）",
        "params": {"backend": "s", "dataset": "s", "srid": "n", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.DefineProjection"),
            "qgis": _proc("native:assignprojection"),
            "postgis": _tpl("set_srid", "UpdateGeometrySRID / ST_SetSRID"),
            "supermap": _unv("native", "数据集坐标系设置（PrjCoordSys）具体接口待验（设计 §2 V14）",
                             native="supermap_assign_projection", wheel="iobjectspy PrjCoordSys 设置（待验）"),
        },
    },
    "gis_reproject": {
        "vid": "V15", "level": "R1", "confirm": "required",
        "semantics": "重投影到新数据集；overwrite=true（覆盖原数据）时升 R3 走额外闸",
        "params": {"backend": "s", "input": "s", "target": "s", "target_srid": "n",
                   "kind": "s", "resampling": "s", "overwrite": "b",
                   "confirm": "b", "target_echo": "s", "preflight_id": "s"},
        "backends": {
            "arcgis-pro": _var("kind", {
                "vector": _gp("arcpy.management.Project"),
                "raster": _gp("arcpy.management.ProjectRaster"),
                "table": _ns("表无坐标，重投影不适用"),
            }),
            "qgis": _var("kind", {
                "vector": _proc("native:reprojectlayer"),
                "raster": _proc("gdal:warpreproject"),
                "table": _ns("表无坐标，重投影不适用"),
            }),
            "postgis": _tpl("transform_create", "ST_Transform 建新表"),
            "supermap": _unv("native", "iobjectspy 投影变换接口普查判 core 但具体名待验（设计 §2 V15）",
                             native="supermap_reproject", wheel="iobjectspy 投影变换（待验）"),
            "gdal": _var("kind", {
                "vector": _nat("gdal_reproject", "ogr2ogr -t_srs", existing=True),
                "raster": _nat("gdal_reproject", "gdalwarp -t_srs", existing=True),
                "table": _ns("表无坐标，重投影不适用"),
            }),
        },
    },
    # ---------------- 格式转换组 ----------------
    "gis_convert_format": {
        "vid": "V16", "level": "R1", "confirm": "required",
        "semantics": "单数据集格式互转（目标格式以驱动名指定）；同语义多轮子按后端环境择一，平台只维护语义映射",
        "params": {"backend": "s", "input": "s", "target": "s", "format": "s",
                   "kind": "s", "confirm": "b"},
        "backends": {
            "qgis": _var("kind", {
                "vector": _proc("gdal:convertformat"),
                "raster": _proc("gdal:translate"),
                "table": _proc("gdal:convertformat"),
            }),
            "arcgis-pro": _var("kind", {
                "vector": dict(_gp("arcpy.conversion.ExportFeatures"),
                               note="按目标格式在 Conversion core 子集内择一（ExportFeatures/FeatureClassToShapefile/FeaturesToJSON 等），桥侧定具体函数"),
                "raster": _gp("arcpy.conversion.RasterToOtherFormat"),
                "table": dict(_gp("arcpy.conversion.ExportFeatures"),
                              note="表导出在 Conversion core 子集内择一，桥侧定具体函数"),
            }),
            "supermap": _nat("supermap_export_data", "iobjectspy.conversion export_*"),
            "gdal": _var("kind", {
                "vector": _nat("gdal_convert_format", "ogr2ogr -f", existing=True),
                "raster": _nat("gdal_convert_format", "gdal_translate -of", existing=True),
                "table": _ns("首版未单独验表格式转换（CSV/表→表），"
                             "不冒充；矢量/栅格两形态已实跑"),
            }),
            "postgis": _var("format", {
                "GeoJSON": _ok("native", native="postgis_export_geojson",
                               bridge_tool_status="existing",
                               wheel="ST_AsGeoJSON 导出（桥既有固定模板）"),
                "*": _ns("PostGIS 只支持表→GeoJSON 类轻量导出；文件级互转未核实，不冒名（设计 §2 V16）"),
            }),
        },
    },
    "gis_import_data": {
        "vid": "V17", "level": "R1", "confirm": "required",
        "semantics": "把外部文件/服务数据导入后端的工作空间或数据库（目标是后端内部数据集）",
        "params": {"backend": "s", "source_uri": "s", "target_name": "s",
                   "format": "s", "kind": "s", "confirm": "b"},
        "backends": {
            "supermap": _nat("supermap_import_data", "iobjectspy.conversion import_*（80+ 格式）"),
            "arcgis-pro": dict(_gp("arcpy.conversion.FeatureClassToGeodatabase"),
                               note="按源格式在 Conversion 的 To Geodatabase 族内择一（RasterToGeodatabase/JSONToFeatures/KMLToLayer 等），桥侧定具体函数"),
            "qgis": dict(_proc("gdal:convertformat"),
                         note="写目标库为近似映射（经 GDAL 转换落库），非原生导入语义"),
            "postgis": _var("kind", {
                "raster": _tpl("from_gdal_raster", "ST_FromGDALRaster（栅格入库）"),
                "vector": _ns("文件级矢量入库走 GDAL ogr2ogr 命令行轮子（平台外工具），登记不冒名（设计 §2 V17）"),
                "table": _ns("文件级表入库未核实，本波不开"),
            }),
        },
    },
    # ---------------- 矢量分析组 ----------------
    "gis_buffer": {
        "vid": "V18", "level": "R1", "confirm": "required",
        "semantics": "按距离生成缓冲区",
        "params": {"backend": "s", "input": "s", "target": "s", "distance": "n",
                   "distance_field": "s", "dissolve": "b", "unit": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.analysis.Buffer"),
            "qgis": _proc("native:buffer"),
            "supermap": _nat("supermap_create_buffer", "iobjectspy.analyst.create_buffer"),
            "postgis": _tpl("buffer_create", "ST_Buffer"),
        },
    },
    "gis_clip": {
        "vid": "V19", "level": "R1", "confirm": "required",
        "semantics": "按裁剪数据集/范围裁剪（矢量/栅格按 input_type 分流）",
        "params": {"backend": "s", "input": "s", "clip_by": "s", "target": "s",
                   "input_type": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _var("input_type", {
                "vector": _gp("arcpy.analysis.Clip"),
                "raster": _gp("arcpy.sa.ExtractByMask"),
            }),
            "qgis": _var("input_type", {
                "vector": _proc("qgis:clip"),
                "raster": _proc("gdal:cliprasterbymasklayer"),
            }),
            "supermap": _var("input_type", {
                "vector": _nat("supermap_overlay_clip", "iobjectspy.analyst.overlay（裁剪明列）"),
                "raster": _nat("supermap_clip_raster", "iobjectspy.analyst.clip_raster"),
            }),
            "postgis": _var("input_type", {
                "vector": _tpl("clip_vector", "ST_Intersection / ST_ClipByBox2D"),
                "raster": _tpl("clip_raster", "ST_Clip"),
            }),
            "gdal": _var("input_type", {
                "vector": _nat("gdal_clip", "ogr2ogr -clipsrc", existing=True),
                "raster": _nat("gdal_clip", "gdalwarp -cutline", existing=True),
            }),
        },
    },
    "gis_overlay": {
        "vid": "V20", "level": "R1", "confirm": "required",
        "semantics": "二元叠加 operation∈{intersect,union,difference,erase,identity,symdifference,update}；后端缺某式时该式回 NOT_SUPPORTED，不许用组合运算冒名替代",
        "params": {"backend": "s", "input": "s", "overlay": "s", "target": "s",
                   "operation": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _var("operation", {
                "intersect": _gp("arcpy.analysis.Intersect"),
                "union": _gp("arcpy.analysis.Union"),
                "difference": dict(_gp("arcpy.analysis.Erase"),
                                   note="difference 语义在 ArcGIS 侧由 Erase 承担（输入减去叠加层）"),
                "erase": _gp("arcpy.analysis.Erase"),
                "identity": _gp("arcpy.analysis.Identity"),
                "symdifference": _gp("arcpy.analysis.SymmetricalDifference"),
                "update": _gp("arcpy.analysis.Update"),
            }),
            "qgis": _var("operation", {
                "intersect": _proc("qgis:intersection"),
                "union": _proc("qgis:union"),
                "difference": _proc("qgis:difference"),
                "erase": dict(_proc("qgis:difference"),
                              note="erase 语义在 QGIS 侧由 difference 承担"),
                "symdifference": _proc("qgis:symmetricaldifference"),
                "identity": _ns("普查 QGIS 清单中无 identity 同名条目，未核实，本波 NOT_SUPPORTED（设计 §2 V20）"),
                "update": _ns("普查 QGIS 清单中无 update 同名条目，未核实，本波 NOT_SUPPORTED（设计 §2 V20）"),
            }),
            "supermap": _var("operation", {
                "intersect": _unv("native", "iobjectspy.analyst.overlay 其余式在 10.1.0 待验，未验前不开（裁剪已明列，走 gis_clip）",
                                  native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "union": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "difference": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "erase": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "identity": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "symdifference": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
                "update": _unv("native", "同 intersect 注", native="supermap_overlay", wheel="iobjectspy.analyst.overlay（待验）"),
            }),
            "postgis": _var("operation", {
                "intersect": _tpl("overlay_intersection", "ST_Intersection"),
                "union": _tpl("overlay_union", "ST_Union"),
                "difference": _tpl("overlay_difference", "ST_Difference"),
                "erase": dict(_tpl("overlay_difference", "ST_Difference"),
                              note="erase 语义在 PostGIS 侧由 ST_Difference 承担"),
                "symdifference": _tpl("overlay_symdifference", "ST_SymDifference"),
                "identity": _ns("无单函数对应，NOT_SUPPORTED（设计 §2 V20）"),
                "update": _ns("无单函数对应，NOT_SUPPORTED（设计 §2 V20）"),
            }),
        },
    },
    "gis_dissolve": {
        "vid": "V21", "level": "R1", "confirm": "required",
        "semantics": "按字段融合相邻/同值要素",
        "params": {"backend": "s", "input": "s", "target": "s", "fields": "a", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.management.Dissolve"),
            "qgis": _proc("native:dissolve"),
            "supermap": _nat("supermap_dissolve", "iobjectspy.analyst 融合（Dissolve）"),
            "postgis": _tpl("dissolve", "ST_Union + GROUP BY"),
        },
    },
    "gis_spatial_join": {
        "vid": "V22", "level": "R1", "confirm": "required",
        "semantics": "按空间谓词把 join 层属性连接进 input 并写出新数据集",
        "params": {"backend": "s", "input": "s", "join": "s", "target": "s",
                   "predicate": "s", "summary": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.analysis.SpatialJoin"),
            "qgis": _proc("native:joinattributesbylocation"),
            "postgis": _var("predicate", {
                "intersects": _tpl("spatial_join", "JOIN + ST_Intersects"),
                "contains": _tpl("spatial_join", "JOIN + ST_Contains"),
                "within": _tpl("spatial_join", "JOIN + ST_Within"),
                "nearest": _ns("最近邻连接需逐行相关子查询模板，未在本波模板集内，登记待补"),
            }),
            "supermap": _ns("iobjectspy.analyst 空间连接未逐项核实，未验前 NOT_SUPPORTED（设计 §2 V22）"),
        },
    },
    # ---------------- 栅格分析组 + PostGIS 服务端集 ----------------
    "gis_raster_calc": {
        "vid": "V23", "level": "R1", "confirm": "required",
        "semantics": "栅格代数计算（表达式语法随后端原生）",
        "params": {"backend": "s", "inputs": "o", "expression": "s", "target": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.sa.RasterCalculator"),
            "qgis": _proc("native:rastercalc"),
            "supermap": _nat("supermap_raster_calc", "iobjectspy.analyst 栅格代数"),
            "postgis": _tpl("mapalgebra", "ST_MapAlgebra（表达式版）"),
        },
    },
    "gis_slope": {
        "vid": "V24", "level": "R1", "confirm": "required",
        "semantics": "由 DEM 计算坡度",
        "params": {"backend": "s", "input": "s", "target": "s", "z_factor": "n", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.sa.Slope"),
            "qgis": _proc("qgis:slope"),
            "supermap": _unv("native", "iobjectspy.analyst 表面分析具体函数名待验（设计 §2 V24）",
                             native="supermap_slope", wheel="iobjectspy.analyst 坡度（待验）"),
            "postgis": _tpl("slope", "ST_Slope"),
            "gdal": _nat("gdal_slope", "gdaldem slope", existing=True),
        },
    },
    "gis_aspect": {
        "vid": "V25", "level": "R1", "confirm": "required",
        "semantics": "由 DEM 计算坡向",
        "params": {"backend": "s", "input": "s", "target": "s", "z_factor": "n", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.sa.Aspect"),
            "qgis": _proc("qgis:aspect"),
            "supermap": _unv("native", "同 gis_slope 注（设计 §2 V25）",
                             native="supermap_aspect", wheel="iobjectspy.analyst 坡向（待验）"),
            "postgis": _tpl("aspect", "ST_Aspect"),
            "gdal": _nat("gdal_aspect", "gdaldem aspect", existing=True),
        },
    },
    "gis_hillshade": {
        "vid": "V26", "level": "R1", "confirm": "required",
        "semantics": "由 DEM 计算山体阴影",
        "params": {"backend": "s", "input": "s", "target": "s", "z_factor": "n", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.sa.Hillshade"),
            "qgis": _proc("qgis:hillshade"),
            "supermap": _unv("native", "同 gis_slope 注（设计 §2 V26）",
                             native="supermap_hillshade", wheel="iobjectspy.analyst 山体阴影（待验）"),
            "postgis": _tpl("hillshade", "ST_HillShade"),
            "gdal": _nat("gdal_hillshade", "gdaldem hillshade", existing=True),
        },
    },
    "gis_reclassify": {
        "vid": "V27", "level": "R1", "confirm": "required",
        "semantics": "按规则表重分类栅格值",
        "params": {"backend": "s", "input": "s", "target": "s", "rules": "a", "confirm": "b"},
        "backends": {
            "arcgis-pro": _unv("gp_named", "Reclassify 函数名按普查命名规则生成，须以 arcpy 实际导入为准（设计 §2 V27）",
                               func="arcpy.sa.Reclassify", wheel="arcpy.sa.Reclassify"),
            "qgis": _proc("native:reclassifybytable"),
            "supermap": _nat("supermap_reclassify", "iobjectspy.analyst 重分类"),
            "postgis": _tpl("reclass", "ST_Reclass"),
        },
    },
    "gis_zonal_statistics": {
        "vid": "V28", "level": "R1", "confirm": "required",
        "semantics": "分区统计（zones × values → 统计表或栅格）",
        "params": {"backend": "s", "zones": "s", "values": "s", "target": "s",
                   "statistics": "a", "output": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.sa.ZonalStatisticsAsTable"),
            "qgis": _proc("native:zonalstatisticsfb"),
            "supermap": _nat("supermap_zonal_statistics", "iobjectspy.analyst 区域统计"),
            "postgis": dict(_tpl("zonal_stats", "ST_SummaryStats + 空间连接（组合模板）"),
                            note="derived：非单函数，由模板组合实现，注册表单独标 derived"),
        },
    },
    "gis_field_statistics": {
        "vid": "V29", "level": "R0", "confirm": "none",
        "semantics": "字段统计（output=result 时 R0；output=stored 落表时升 R1 需 confirm）",
        "params": {"backend": "s", "dataset": "s", "fields": "a", "group_by": "a",
                   "statistics": "a", "output": "s", "target": "s", "confirm": "b"},
        "backends": {
            "arcgis-pro": _gp("arcpy.analysis.SummaryStatistics"),
            "qgis": _proc("qgis:basicstatisticsforfields"),
            "postgis": _tpl("field_stats", "SQL 聚合模板"),
            "supermap": _ns("iobjectspy.analyst 统计类具体名待验，未验前 NOT_SUPPORTED（设计 §2 V29）"),
        },
    },
    "gis_spatial_filter": {
        "vid": "V30", "level": "R0", "confirm": "none",
        "semantics": "PostGIS 服务端空间谓词过滤查要素子集（谓词封闭枚举，禁止裸 SQL）",
        "params": {"backend": "s", "table": "s", "predicate": "s", "reference_wkt": "s",
                   "reference_table": "s", "distance": "n", "limit": "n"},
        "backends": {
            "postgis": _tpl("spatial_filter", "ST_Intersects/ST_Contains/ST_Within/ST_DWithin + && 索引运算符"),
        },
    },
    "gis_measure": {
        "vid": "V31", "level": "R0", "confirm": "none",
        "semantics": "量测：距离/面积/长度/方位角（标量回包，不落表）",
        "params": {"backend": "s", "operation": "s", "a_wkt": "s", "b_wkt": "s",
                   "srid": "n", "use_geography": "b"},
        "backends": {
            "postgis": _var("operation", {
                "distance": _tpl("measure_distance", "ST_Distance"),
                "area": _tpl("measure_area", "ST_Area"),
                "length": _tpl("measure_length", "ST_Length"),
                "azimuth": _tpl("measure_azimuth", "ST_Azimuth"),
            }),
        },
    },
    "gis_validate_geometry": {
        "vid": "V32", "level": "R0", "confirm": "none",
        "semantics": "几何有效性校验（repair=true 时升 R2 原地修复，需 confirm）",
        "params": {"backend": "s", "dataset": "s", "repair": "b", "confirm": "b"},
        "backends": {
            "postgis": {
                "check": dict(
                    _tpl("validate_check", "ST_IsValid / ST_IsValidReason"),
                    note="2026-11-03 实机校准定版：validate_check 在真实 PostGIS "
                         "38/38 PASS；网关执行器 postgis_exec_template 仍 pending"),
                "repair": dict(
                    _tpl("validate_repair", "ST_MakeValid"),
                    note="2026-11-03 实机校准定版：validate_repair 输出新表形态，"
                         "真实 PostGIS 38/38 PASS；网关执行器仍 pending")},
            "arcgis-pro": {
                "check": _unv(
                    "gp_named",
                    "阶段 1 裁决（2026-11-05）：GP 注册表/白名单在册，但无 Pro "
                    "环境、未实机；与 leaves 账本 unverified 对齐",
                    func="arcpy.management.CheckGeometry",
                    wheel="arcpy.management.CheckGeometry"),
                "repair": _unv(
                    "gp_named",
                    "阶段 1 裁决（2026-11-05）：GP 注册表/白名单在册，但无 Pro "
                    "环境、未实机；与 leaves 账本 unverified 对齐",
                    func="arcpy.management.RepairGeometry",
                    wheel="arcpy.management.RepairGeometry")},
            "qgis": {
                "check": _unv(
                    "processing",
                    "阶段 1 裁决（2026-11-05）：Processing 种子账仅名级，未实机；"
                    "与 leaves 账本 unverified 对齐",
                    algorithm="qgis:checkvalidity", wheel="qgis:checkvalidity"),
                "repair": _unv(
                    "processing",
                    "阶段 1 裁决（2026-11-05）：Processing 种子账仅名级，未实机；"
                    "与 leaves 账本 unverified 对齐",
                    algorithm="native:fixgeometries",
                    wheel="native:fixgeometries")},
            "supermap": _ns(
                "B1/D5 2026-11-03 name_verified_function: topology_validate；"
                "本波维持 NOT_SUPPORTED（设计 §2 V32），不冒充可执行"),
        },
    },
    "gis_serve_vector_tile": {
        "vid": "V33", "level": "R0", "confirm": "none",
        "semantics": "按 XYZ 直出 MVT 矢量瓦片（回包为二进制句柄，不进 JSON 文本面）",
        "params": {"backend": "s", "table": "s", "z": "n", "x": "n", "y": "n",
                   "geometry_column": "s", "attributes": "a"},
        "backends": {
            "postgis": _tpl("mvt_tile", "ST_AsMVT + ST_AsMVTGeom + ST_TileEnvelope"),
        },
    },
    # ---------------- 发布与服务组 ----------------
    "gis_publish_layer": {
        "vid": "V34", "level": "R1", "confirm": "required",
        "semantics": "经 GeoServer REST 发布链把数据集发布为图层（许可闸前置：catalog 来源先查许可）；发布成功回写目录发布记录（catalog 回写工具未就绪前回包标 pending）",
        "params": {"backend": "s", "dataset_ref": "s", "workspace": "s",
                   "style": "s", "purpose": "s", "confirm": "b"},
        "backends": {
            "geoserver": dict(_nat("geoserver_publish_layer",
                                   "REST 发布链 workspaces→datastores/coveragestores→featuretypes/coverages→layers/styles"),
                              note=PENDING_NOTE),
        },
    },
    "gis_list_services": {
        "vid": "V35", "level": "R0", "confirm": "none",
        "semantics": "列服务后端的 OGC 服务与能力摘要（discover 看后端与许可，本动词看服务面）",
        "params": {"backend": "s", "service": "s"},
        "backends": {
            "geoserver": _ok("native", native="geoserver_capabilities_summary",
                             bridge_tool_status="existing",
                             wheel="WMS/WFS GetCapabilities 摘要"),
            "istsos": dict(_nat("istsos_service_root", "STA 服务根实体集索引"),
                           note=PENDING_NOTE),
            "supermap": _ns("iServer 服务面本波登记，NOT_SUPPORTED（设计 §2 V35）"),
            "iserver": _ok(
                "native", native="iserver_list_services",
                bridge_tool_status="existing",
                wheel="GET /iserver/services.json",
                note="demo-instance-verified：官方公开演示实例（非本机、"
                     "版本未确认）；仅 GET；服务目录 115；"
                     "map-china/data-china 已确认；spatial 根/子资源"
                     "形状已确认，执行未尝试"),
        },
    },
    # ---------------- 时序观测组 ----------------
    "gis_query_observations": {
        "vid": "V36", "level": "R0", "confirm": "none",
        "semantics": "STA 实体读全集（8 实体）＋ OData 查询下推（参数字段透传，不在网关本地过滤冒充下推）；写面本波不开",
        "params": {"backend": "s", "entity": "s", "datastream_id": "n", "thing_id": "n",
                   "filter": "s", "top": "n", "skip": "n", "count": "b",
                   "expand": "s", "select": "s", "orderby": "s"},
        "backends": {
            "istsos": _var("entity", {
                "Things": _ok("native", native="istsos_list_things",
                              bridge_tool_status="existing", wheel="STA GET /Things"),
                "Datastreams": _ok("native", native="istsos_list_datastreams",
                                   bridge_tool_status="existing", wheel="STA GET /Datastreams"),
                "Observations": _ok("native", native="istsos_get_observations",
                                    bridge_tool_status="existing",
                                    wheel="STA GET /Datastreams(id)/Observations（须 datastream_id）"),
                "Locations": dict(_nat("istsos_query_entities", "STA GET /Locations"),
                                  note=PENDING_NOTE),
                "HistoricalLocations": dict(_nat("istsos_query_entities", "STA GET /HistoricalLocations"),
                                            note=PENDING_NOTE),
                "Sensors": dict(_nat("istsos_query_entities", "STA GET /Sensors"),
                                note=PENDING_NOTE),
                "ObservedProperties": dict(_nat("istsos_query_entities", "STA GET /ObservedProperties"),
                                           note=PENDING_NOTE),
                "FeaturesOfInterest": dict(_nat("istsos_query_entities", "STA GET /FeaturesOfInterest"),
                                           note=PENDING_NOTE),
            }),
        },
    },
    # ---------------- 点云组 ----------------
    "gis_pointcloud_info": {
        "vid": "V37", "level": "R0", "confirm": "none",
        "semantics": "点云信息（PDAL info）",
        "params": {"backend": "s", "input": "s"},
        "backends": {
            "qgis": _proc("pdal:info"),
        },
    },
    "gis_pointcloud_process": {
        "vid": "V38", "level": "R1", "confirm": "required",
        "semantics": "点云处理（PDAL 试点）：clip/reproject/thin_*/merge/convert/export_raster*/density/boundary 按 action 分流到 PDAL 算法",
        "params": {"backend": "s", "input": "s", "target": "s", "action": "s",
                   "params": "o", "confirm": "b"},
        "backends": {
            "qgis": _var("action", {
                "clip": _proc("pdal:clip"),
                "reproject": _proc("pdal:reproject"),
                "thin_radius": _proc("pdal:thinbyradius"),
                "thin_decimate": _proc("pdal:thinbydecimate"),
                "merge": _proc("pdal:merge"),
                "convert": _proc("pdal:convertformat"),
                "export_raster": _proc("pdal:exportraster"),
                "export_raster_tin": _proc("pdal:exportrastertin"),
                "density": _proc("pdal:density"),
                "boundary": _proc("pdal:boundary"),
            }),
        },
    },
    # ---------------- 目录链路与出图组 ----------------
    "gis_add_layer_from_catalog": {
        "vid": "V39", "level": "R1", "confirm": "required",
        "semantics": "「按目录找数据 → 加图层」链路：取 catalog dataset 的 storage.uri 加进目标 GIS 工程当前地图；许可闸前置（无 evidence_ref、或 commercial_use 与用途冲突时回 LICENSE_BLOCKED）",
        "params": {"backend": "s", "catalog_id": "s", "map": "s",
                   "purpose": "s", "confirm": "b"},
        "backends": {
            "supermap": dict(_ok("native", native="supermap_add_dataset_to_map",
                                 bridge_tool_status="existing",
                                 wheel="桥既有 add_dataset_to_map"),
                             note="目录登记 id 作为数据集名透传，实机以工作空间内实际名为准"),
            "arcgis-pro": _ok("native", native="arcgis_add_layer_from_path",
                              bridge_tool_status="existing",
                              wheel="桥既有 add_layer_from_path（path=storage.uri）"),
            "qgis": _ok("native", native="qgis_add_layer_from_path",
                        bridge_tool_status="existing",
                        wheel="桥既有 add_layer_from_path（path=storage.uri）"),
            "catalog": _ns("目录后端自身不开此动词（目标必须是 GIS 后端）"),
        },
    },
    "gis_export_map_image": {
        "vid": "V40", "level": "R1", "confirm": "bridge",
        "semantics": "当前地图/布局导出图片（各桥既有出图工具升入统一面）；PDF 批量图集类不在内（defer）",
        "params": {"backend": "s", "map": "s", "layout": "s", "target_path": "s",
                   "format": "s", "dpi": "n", "confirm": "b"},
        "backends": {
            "supermap": _ok("native", native="supermap_export_map_image",
                            bridge_tool_status="existing", wheel="桥既有 export_map_image"),
            "arcgis-pro": _ok("native", native="arcgis_export_map_image",
                              bridge_tool_status="existing", wheel="桥既有 export_map_image"),
            "arcmap": _ns("ArcMap 冻结存量（D3/派单口径）：桥内有 arcmap_export_map_image，本波不升统一面"),
            "qgis": _ok("native", native="qgis_export_map_image",
                        bridge_tool_status="existing", wheel="桥既有 export_map_image"),
        },
    },
}

VERB_ORDER = ["gis_run_gp", "gis_run_processing", "gis_list_algorithms",
              "gis_describe_algorithm", "gis_create_dataset", "gis_add_field",
              "gis_delete_field", "gis_calculate_field", "gis_copy_dataset",
              "gis_rename_dataset", "gis_delete_dataset", "gis_merge_datasets",
              "gis_append_dataset", "gis_assign_projection", "gis_reproject",
              "gis_convert_format", "gis_import_data", "gis_buffer", "gis_clip",
              "gis_overlay", "gis_dissolve", "gis_spatial_join",
              "gis_raster_calc", "gis_slope", "gis_aspect", "gis_hillshade",
              "gis_reclassify", "gis_zonal_statistics", "gis_field_statistics",
              "gis_spatial_filter", "gis_measure", "gis_validate_geometry",
              "gis_serve_vector_tile", "gis_publish_layer", "gis_list_services",
              "gis_query_observations", "gis_pointcloud_info",
              "gis_pointcloud_process", "gis_add_layer_from_catalog",
              "gis_export_map_image"]


# =====================================================================
# 第三部分：PostGIS 参数化模板集（设计 §3.3）
# =====================================================================
# 占位符纪律：{ident:x}=标识符槽（网关过 ^[A-Za-z_][A-Za-z0-9_]*$ 正则、
# 表名许 schema. 前缀后才拼入）；{idents:x}=标识符列表槽；{enum:x}=封闭
# 枚举槽（白名单校验后拼入）；%(x)s=绑定值参数（永不拼进 SQL 文本）。
# {expr:x}=受限表达式片段槽（仅 update_field 用：单表达式，禁分号与
# DDL/DML 关键字，网关校验；这是设计 §2 V08 明定的「表达式语言随后端」
# 口径，不是裸 SQL 通道——平台不开任何 gis_run_sql 类动词）。

def _t(tid, verbs, level, desc, sql, params, **kw):
    d = {"template_id": tid, "verbs": verbs, "level": level,
         "description": desc, "sql": sql, "params": params}
    d.update(kw)
    return d


def _p(kind, **kw):
    d = {"kind": kind}
    d.update(kw)
    return d


_ID = _p("ident_table")
_IDC = _p("ident_column")
_VAL = _p("value")

TEMPLATES = [
    _t("create_table", ["gis_create_dataset"], "R1",
       "建表＋几何列（几何类型名走封闭枚举，SRID 走绑定参数；附加字段经 gis_add_field 逐个加）",
       "CREATE TABLE {ident:table} ({ident:id_column} serial PRIMARY KEY, "
       "{ident:geometry_column} geometry({enum:geometry_type}, %(srid)s))",
       {"table": _ID, "id_column": dict(_IDC, default="id"),
        "geometry_column": dict(_IDC, default="geom"),
        "geometry_type": _p("enum", values=["Point", "LineString", "Polygon",
                                            "MultiPoint", "MultiLineString",
                                            "MultiPolygon", "Geometry"],
                            default="Geometry"),
        "srid": dict(_VAL, default=4326)}),
    _t("add_column", ["gis_add_field"], "R2", "加字段（类型走封闭枚举）",
       "ALTER TABLE {ident:table} ADD COLUMN {ident:column} {enum:sql_type}",
       {"table": _ID, "column": _IDC,
        "sql_type": _p("enum", values=["text", "integer", "bigint",
                                       "double precision", "boolean", "date",
                                       "timestamp", "numeric"])}),
    _t("drop_column", ["gis_delete_field"], "R3", "删字段（R3 额外闸在网关层）",
       "ALTER TABLE {ident:table} DROP COLUMN {ident:column}",
       {"table": _ID, "column": _IDC}),
    _t("update_field", ["gis_calculate_field"], "R2",
       "字段计算：表达式为受限片段槽（单表达式；禁分号、禁 DDL/DML 关键字），其余全绑定/标识符校验",
       "UPDATE {ident:table} SET {ident:column} = {expr:expression}",
       {"table": _ID, "column": _IDC, "expression": _p("expression")}),
    _t("copy_table", ["gis_copy_dataset"], "R1", "复制表为新表",
       "CREATE TABLE {ident:target} AS SELECT * FROM {ident:source}",
       {"target": _ID, "source": _ID}),
    _t("rename_table", ["gis_rename_dataset"], "R2", "表重命名",
       "ALTER TABLE {ident:table} RENAME TO {ident:new_name}",
       {"table": _ID, "new_name": _IDC}),
    _t("drop_table", ["gis_delete_dataset"], "R3", "删表（R3 额外闸在网关层）",
       "DROP TABLE {ident:table}", {"table": _ID}),
    _t("merge_tables", ["gis_merge_datasets"], "R1", "多表 UNION ALL 建新表（inputs 每项过标识符校验后逐项拼入）",
       "CREATE TABLE {ident:target} AS {union_all:inputs}",
       {"target": _ID, "inputs": _p("ident_tables")}, builder="union_all"),
    _t("insert_select", ["gis_append_dataset"], "R2", "追加：INSERT INTO … SELECT",
       "INSERT INTO {ident:target} SELECT * FROM {ident:source}",
       {"target": _ID, "source": _ID}),
    _t("set_srid", ["gis_assign_projection"], "R2",
       "定义 SRID（只改元数据）：表名/列名在此以字符串值绑定传入 UpdateGeometrySRID",
       "SELECT UpdateGeometrySRID(%(table)s, %(column)s, %(srid)s)",
       {"table": _VAL, "column": dict(_VAL, default="geom"),
        "srid": _VAL}),
    _t("transform_create", ["gis_reproject"], "R1",
       "重投影建新表（本模板只带几何列，属性列扩展在桥侧模板迭代时补，登记注记）",
       "CREATE TABLE {ident:target} AS SELECT ST_Transform({ident:geometry_column}, "
       "%(target_srid)s) AS {ident:geometry_column} FROM {ident:source}",
       {"target": _ID, "source": _ID,
        "geometry_column": dict(_IDC, default="geom"), "target_srid": _VAL}),
    _t("from_gdal_raster", ["gis_import_data"], "R1", "栅格入库（文件路径走绑定参数）",
       "CREATE TABLE {ident:target} AS SELECT ST_FromGDALRaster(%(file_path)s) AS rast",
       {"target": _ID, "file_path": _VAL}),
    _t("buffer_create", ["gis_buffer"], "R1", "缓冲建新表（距离绑定参数）",
       "CREATE TABLE {ident:target} AS SELECT *, ST_Buffer({ident:geometry_column}, "
       "%(distance)s) AS geom_buffered FROM {ident:source}",
       {"target": _ID, "source": _ID,
        "geometry_column": dict(_IDC, default="geom"), "distance": _VAL}),
    _t("clip_vector", ["gis_clip"], "R1", "矢量裁剪（与裁剪表相交并取交集几何）",
       "CREATE TABLE {ident:target} AS SELECT a.*, "
       "ST_Intersection(a.{ident:geometry_column}, b.{ident:geometry_column}) AS geom_clipped "
       "FROM {ident:source} a JOIN {ident:clip_table} b "
       "ON ST_Intersects(a.{ident:geometry_column}, b.{ident:geometry_column})",
       {"target": _ID, "source": _ID, "clip_table": _ID,
        "geometry_column": dict(_IDC, default="geom")}),
    _t("clip_raster", ["gis_clip"], "R1",
       "栅格裁剪：clip_by 为 WKT 时用绑定几何；为表名时网关改走 sql_table_clip 形态",
       "CREATE TABLE {ident:target} AS SELECT ST_Clip(rast, %(band)s, "
       "ST_GeomFromText(%(clip_wkt)s, %(srid)s)) AS rast FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1),
        "clip_wkt": _VAL, "srid": dict(_VAL, default=4326),
        "clip_table": _ID, "geometry_column": dict(_IDC, default="geom")},
       sql_table_clip="CREATE TABLE {ident:target} AS SELECT ST_Clip(a.rast, "
                      "b.{ident:geometry_column}) AS rast FROM {ident:source} a, "
                      "{ident:clip_table} b"),
    _t("overlay_intersection", ["gis_overlay"], "R1", "叠加·相交",
       "CREATE TABLE {ident:target} AS SELECT "
       "ST_Intersection(a.{ident:geometry_column}, b.{ident:geometry_column}) AS geom "
       "FROM {ident:source} a JOIN {ident:overlay_table} b "
       "ON ST_Intersects(a.{ident:geometry_column}, b.{ident:geometry_column})",
       {"target": _ID, "source": _ID, "overlay_table": _ID,
        "geometry_column": dict(_IDC, default="geom")}),
    _t("overlay_union", ["gis_overlay"], "R1", "叠加·并集（聚合）",
       "CREATE TABLE {ident:target} AS SELECT ST_Union(g) AS geom FROM "
       "(SELECT {ident:geometry_column} AS g FROM {ident:source} "
       "UNION ALL SELECT {ident:geometry_column} FROM {ident:overlay_table}) u",
       {"target": _ID, "source": _ID, "overlay_table": _ID,
        "geometry_column": dict(_IDC, default="geom")}),
    _t("overlay_difference", ["gis_overlay"], "R1", "叠加·差集（difference/erase）",
       "CREATE TABLE {ident:target} AS SELECT ST_Difference(a.{ident:geometry_column}, "
       "(SELECT ST_Union({ident:geometry_column}) FROM {ident:overlay_table})) AS geom "
       "FROM {ident:source} a",
       {"target": _ID, "source": _ID, "overlay_table": _ID,
        "geometry_column": dict(_IDC, default="geom")}),
    _t("overlay_symdifference", ["gis_overlay"], "R1", "叠加·对称差",
       "CREATE TABLE {ident:target} AS SELECT ST_SymDifference(a.{ident:geometry_column}, "
       "(SELECT ST_Union({ident:geometry_column}) FROM {ident:overlay_table})) AS geom "
       "FROM {ident:source} a",
       {"target": _ID, "source": _ID, "overlay_table": _ID,
        "geometry_column": dict(_IDC, default="geom")}),
    _t("dissolve", ["gis_dissolve"], "R1", "融合：ST_Union + GROUP BY（无分组字段时走 sql_nogroup）",
       "CREATE TABLE {ident:target} AS SELECT {idents:group_columns}, "
       "ST_Union({ident:geometry_column}) AS geom FROM {ident:source} "
       "GROUP BY {idents:group_columns}",
       {"target": _ID, "source": _ID,
        "group_columns": _p("ident_columns"),
        "geometry_column": dict(_IDC, default="geom")},
       sql_nogroup="CREATE TABLE {ident:target} AS SELECT "
                   "ST_Union({ident:geometry_column}) AS geom FROM {ident:source}"),
    _t("spatial_join", ["gis_spatial_join"], "R1", "空间连接（谓词走 fragments 封闭映射）",
       "CREATE TABLE {ident:target} AS SELECT a.*, b.* FROM {ident:source} a "
       "JOIN {ident:join_table} b ON {fragment:predicate}",
       {"target": _ID, "source": _ID, "join_table": _ID,
        "geometry_column": dict(_IDC, default="geom"),
        "predicate": _p("enum", values=["intersects", "contains", "within"])},
       fragments={"predicate": {
           "intersects": "ST_Intersects(a.{ident:geometry_column}, b.{ident:geometry_column})",
           "contains": "ST_Contains(a.{ident:geometry_column}, b.{ident:geometry_column})",
           "within": "ST_Within(a.{ident:geometry_column}, b.{ident:geometry_column})"}}),
    _t("mapalgebra", ["gis_raster_calc"], "R1", "栅格代数（表达式文本作为绑定值传给 ST_MapAlgebra）",
       "CREATE TABLE {ident:target} AS SELECT ST_MapAlgebra(rast, %(band)s, "
       "%(expression)s) AS rast FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1),
        "expression": _VAL}),
    _t("slope", ["gis_slope"], "R1", "坡度",
       "CREATE TABLE {ident:target} AS SELECT ST_Slope(rast, %(band)s) AS rast "
       "FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1)}),
    _t("aspect", ["gis_aspect"], "R1", "坡向",
       "CREATE TABLE {ident:target} AS SELECT ST_Aspect(rast, %(band)s) AS rast "
       "FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1)}),
    _t("hillshade", ["gis_hillshade"], "R1", "山体阴影（方位角/高度角带默认值）",
       "CREATE TABLE {ident:target} AS SELECT ST_HillShade(rast, %(band)s, "
       "%(azimuth)s, %(altitude)s) AS rast FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1),
        "azimuth": dict(_VAL, default=315), "altitude": dict(_VAL, default=45)}),
    _t("reclass", ["gis_reclassify"], "R1", "重分类（reclassarg 由网关按 rules 数值校验后拼成字符串再绑定）",
       "CREATE TABLE {ident:target} AS SELECT ST_Reclass(rast, %(band)s, "
       "%(reclassarg)s) AS rast FROM {ident:source}",
       {"target": _ID, "source": _ID, "band": dict(_VAL, default=1),
        "reclassarg": _VAL}),
    _t("zonal_stats", ["gis_zonal_statistics"], "R1",
       "分区统计（derived 组合模板：ST_Clip+ST_Union+ST_SummaryStats；统计列全集输出，桥侧按 statistics 裁剪）",
       "CREATE TABLE {ident:target} AS SELECT z.{ident:zone_column} AS zone, "
       "s.count, s.sum, s.mean, s.max, s.min FROM {ident:zones_table} z "
       "JOIN LATERAL (SELECT (ST_SummaryStats(ST_Union(ST_Clip(r.rast, "
       "z.{ident:geometry_column})))).* FROM {ident:values_table} r) s ON true",
       {"target": _ID, "zones_table": _ID, "values_table": _ID,
        "zone_column": dict(_IDC, default="id"),
        "geometry_column": dict(_IDC, default="geom")}),
    _t("field_stats", ["gis_field_statistics"], "R0/R1",
       "字段统计：统计量走封闭枚举 fragments、字段走标识符校验，由网关 builder 拼 SELECT 列",
       "", {"table": _ID, "fields": _p("ident_columns"),
            "group_by": _p("ident_columns"),
            "statistics": _p("enum_list", values=["count", "sum", "avg",
                                                  "min", "max"])},
       builder="field_stats"),
    _t("spatial_filter", ["gis_spatial_filter"], "R0",
       "空间谓词过滤：谓词走 fragments 封闭映射，参考几何 WKT/距离全绑定参数",
       "", {"table": _ID,
            "predicate": _p("enum", values=["intersects", "contains",
                                            "within", "dwithin"]),
            "reference_wkt": _VAL, "reference_table": _ID,
            "distance": _VAL, "limit": dict(_VAL, default=1000),
            "srid": dict(_VAL, default=4326),
            "geometry_column": dict(_IDC, default="geom")},
       builder="spatial_filter"),
    _t("measure_distance", ["gis_measure"], "R0", "两几何距离（WKT 全绑定）",
       "SELECT ST_Distance(ST_GeomFromText(%(a_wkt)s, %(srid)s), "
       "ST_GeomFromText(%(b_wkt)s, %(srid)s)) AS value",
       {"a_wkt": _VAL, "b_wkt": _VAL, "srid": dict(_VAL, default=4326)}),
    _t("measure_area", ["gis_measure"], "R0", "面积",
       "SELECT ST_Area(ST_GeomFromText(%(a_wkt)s, %(srid)s)) AS value",
       {"a_wkt": _VAL, "srid": dict(_VAL, default=4326)}),
    _t("measure_length", ["gis_measure"], "R0", "长度",
       "SELECT ST_Length(ST_GeomFromText(%(a_wkt)s, %(srid)s)) AS value",
       {"a_wkt": _VAL, "srid": dict(_VAL, default=4326)}),
    _t("measure_azimuth", ["gis_measure"], "R0", "方位角",
       "SELECT ST_Azimuth(ST_GeomFromText(%(a_wkt)s, %(srid)s), "
       "ST_GeomFromText(%(b_wkt)s, %(srid)s)) AS value",
       {"a_wkt": _VAL, "b_wkt": _VAL, "srid": dict(_VAL, default=4326)}),
    _t("validate_check", ["gis_validate_geometry"], "R0", "有效性计数校验",
       "SELECT count(*) AS total, count(*) FILTER (WHERE NOT "
       "ST_IsValid({ident:geometry_column})) AS invalid_count FROM {ident:table}",
       {"table": _ID, "geometry_column": dict(_IDC, default="geom")}),
    _t("validate_repair", ["gis_validate_geometry"], "R2", "ST_MakeValid 原地修复无效几何",
       "UPDATE {ident:table} SET {ident:geometry_column} = "
       "ST_MakeValid({ident:geometry_column}) "
       "WHERE NOT ST_IsValid({ident:geometry_column})",
       {"table": _ID, "geometry_column": dict(_IDC, default="geom")}),
    _t("mvt_tile", ["gis_serve_vector_tile"], "R0",
       "MVT 瓦片直出：z/x/y 与图层名全绑定，属性列走标识符校验",
       "SELECT ST_AsMVT(q, %(layer_name)s, 4096, 'geom') AS tile FROM "
       "(SELECT ST_AsMVTGeom({ident:geometry_column}, "
       "ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) AS geom{attr_columns} "
       "FROM {ident:table} WHERE {ident:geometry_column} && "
       "ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) q",
       {"table": _ID, "geometry_column": dict(_IDC, default="geom"),
        "layer_name": _VAL, "z": _VAL, "x": _VAL, "y": _VAL,
        "attributes": _p("ident_columns")}, builder="mvt_tile"),
]

# 2026-11-03 实机校准定版（7 条）：生成器源必须与在册 postgis_templates.json
# 保持一致，防止任何人按 README 重跑时把校准修复静默打回旧版。
CALIBRATED_TEMPLATES = {'clip_raster': {'template_id': 'clip_raster',
                 'verbs': ['gis_clip'],
                 'level': 'R1',
                 'description': '栅格裁剪：clip_by 为 WKT 时用绑定几何；为表名时网关改走 sql_table_clip 形态（2026-11-03 '
                                '实机校准修复：ST_Clip 显式传 crop=true。）',
                 'sql': 'CREATE TABLE {ident:target} AS SELECT ST_Clip(rast, %(band)s, '
                        'ST_GeomFromText(%(clip_wkt)s, %(srid)s), true) AS rast FROM '
                        '{ident:source}',
                 'params': {'target': {'kind': 'ident_table'},
                            'source': {'kind': 'ident_table'},
                            'band': {'kind': 'value', 'default': 1},
                            'clip_wkt': {'kind': 'value'},
                            'srid': {'kind': 'value', 'default': 4326},
                            'clip_table': {'kind': 'ident_table'},
                            'geometry_column': {'kind': 'ident_column', 'default': 'geom'}},
                 'sql_table_clip': 'CREATE TABLE {ident:target} AS SELECT ST_Clip(a.rast, '
                                   'b.{ident:geometry_column}, true) AS rast FROM {ident:source} '
                                   'a, {ident:clip_table} b'},
 'spatial_join': {'template_id': 'spatial_join',
                  'verbs': ['gis_spatial_join'],
                  'level': 'R1',
                  'description': '空间连接（谓词走 fragments 封闭映射；连接表属性须由 attributes 显式列出，带出列别名为 '
                                 'join_<列名>、连接表几何为 join_geom，避免与源表同名列冲突——2026-11-03 实机校准定版，原 a.*, '
                                 'b.* 写法在同名列时建表失败）',
                  'sql': '',
                  'params': {'target': {'kind': 'ident_table'},
                             'source': {'kind': 'ident_table'},
                             'join_table': {'kind': 'ident_table'},
                             'geometry_column': {'kind': 'ident_column', 'default': 'geom'},
                             'predicate': {'kind': 'enum',
                                           'values': ['intersects', 'contains', 'within']},
                             'attributes': {'kind': 'ident_columns'}},
                  'fragments': {'predicate': {'intersects': 'ST_Intersects(a.{ident:geometry_column}, '
                                                            'b.{ident:geometry_column})',
                                              'contains': 'ST_Contains(a.{ident:geometry_column}, '
                                                          'b.{ident:geometry_column})',
                                              'within': 'ST_Within(a.{ident:geometry_column}, '
                                                        'b.{ident:geometry_column})'}},
                  'builder': 'spatial_join'},
 'mapalgebra': {'template_id': 'mapalgebra',
                'verbs': ['gis_raster_calc'],
                'level': 'R1',
                'description': '栅格代数（ST_MapAlgebraExpr；表达式语法为 [rast.val]，文本作绑定值传入。2026-11-03 '
                               '实机校准修复：原 ST_MapAlgebra＋[rast] 写法在 PostGIS 3.4 不成立。）',
                'sql': 'CREATE TABLE {ident:target} AS SELECT ST_MapAlgebraExpr(rast, %(band)s, '
                       '%(pixeltype)s, %(expression)s) AS rast FROM {ident:source}',
                'params': {'target': {'kind': 'ident_table'},
                           'source': {'kind': 'ident_table'},
                           'band': {'kind': 'value', 'default': 1},
                           'expression': {'kind': 'value'},
                           'pixeltype': {'kind': 'value', 'default': '32BF'}}},
 'hillshade': {'template_id': 'hillshade',
               'verbs': ['gis_hillshade'],
               'level': 'R1',
               'description': '山体阴影（方位角/高度角带默认值）（2026-11-03 实机校准修复：补 pixeltype 参数，原调用无匹配签名。）',
               'sql': 'CREATE TABLE {ident:target} AS SELECT ST_HillShade(rast, %(band)s, '
                      '%(pixeltype)s, %(azimuth)s, %(altitude)s) AS rast FROM {ident:source}',
               'params': {'target': {'kind': 'ident_table'},
                          'source': {'kind': 'ident_table'},
                          'band': {'kind': 'value', 'default': 1},
                          'azimuth': {'kind': 'value', 'default': 315},
                          'altitude': {'kind': 'value', 'default': 45},
                          'pixeltype': {'kind': 'value', 'default': '32BF'}}},
 'reclass': {'template_id': 'reclass',
             'verbs': ['gis_reclassify'],
             'level': 'R1',
             'description': '重分类（reclassarg 由网关按 rules 数值校验后拼成字符串再绑定）（2026-11-03 实机校准修复：补 '
                            'pixeltype 参数。）',
             'sql': 'CREATE TABLE {ident:target} AS SELECT ST_Reclass(rast, %(band)s, '
                    '%(reclassarg)s, %(pixeltype)s) AS rast FROM {ident:source}',
             'params': {'target': {'kind': 'ident_table'},
                        'source': {'kind': 'ident_table'},
                        'band': {'kind': 'value', 'default': 1},
                        'reclassarg': {'kind': 'value'},
                        'pixeltype': {'kind': 'value', 'default': '32BF'}}},
 'validate_repair': {'template_id': 'validate_repair',
                     'verbs': ['gis_validate_geometry'],
                     'level': 'R2',
                     'description': '几何修复（输出新表）：修复后几何写入 <几何列>_repaired 列，原表不动。2026-11-03 实机校准定版：原地 '
                                    'UPDATE 在强类型几何列上会因 ST_MakeValid '
                                    '改变几何类型（Polygon→MultiPolygon）而失败，故改为输出新表形态。',
                     'sql': 'CREATE TABLE {ident:target} AS SELECT *, '
                            'ST_MakeValid({ident:geometry_column}) AS '
                            '{ident:geometry_column}_repaired FROM {ident:table}',
                     'params': {'table': {'kind': 'ident_table'},
                                'geometry_column': {'kind': 'ident_column', 'default': 'geom'},
                                'target': {'kind': 'ident_table'}}},
 'mvt_tile': {'template_id': 'mvt_tile',
              'verbs': ['gis_serve_vector_tile'],
              'level': 'R0',
              'description': 'MVT 瓦片直出：z/x/y 与图层名全绑定，属性列走标识符校验（2026-11-03 实机校准修复：槽位须带 :attributes '
                             '后缀；原误标的 builder 字段已去除，走通用替换路径。）',
              'sql': "SELECT ST_AsMVT(q, %(layer_name)s, 4096, 'geom') AS tile FROM (SELECT "
                     'ST_AsMVTGeom({ident:geometry_column}, ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) '
                     'AS geom{attr_columns:attributes} FROM {ident:table} WHERE '
                     '{ident:geometry_column} && ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) q',
              'params': {'table': {'kind': 'ident_table'},
                         'geometry_column': {'kind': 'ident_column', 'default': 'geom'},
                         'layer_name': {'kind': 'value'},
                         'z': {'kind': 'value'},
                         'x': {'kind': 'value'},
                         'y': {'kind': 'value'},
                         'attributes': {'kind': 'ident_columns'}}}}

# 校准覆盖层：以在册定版对象替换旧定义，其余模板保持原顺序。
TEMPLATES = [CALIBRATED_TEMPLATES.get(t["template_id"], t)
             for t in TEMPLATES]
TEMPLATE_BY_ID = {t["template_id"]: t for t in TEMPLATES}


# =====================================================================
# 第四部分：普查解析（注册表真源种子）
# =====================================================================

GP_FN_RE = re.compile(r"arcpy\.[a-z][\w]*\.[A-Z][\w]*")
GP_BATCH1_TOOLBOXES = ("Analysis", "Conversion", "Data Management")
GP_R2_FUNCS = {"arcpy.analysis.Near", "arcpy.analysis.Update",
               "arcpy.management.Append", "arcpy.management.CalculateField",
               "arcpy.management.CalculateFields"}
GP_DOC_ANCHOR_34 = {"Analysis", "Conversion", "Cartography",
                    "Spatial Analyst", "3D Analyst",
                    "Geostatistical Analyst", "Image Analyst",
                    "Network Analyst", "Spatial Statistics",
                    "Space Time Pattern Mining", "Editing", "Geocoding",
                    "Linear Referencing", "Multidimension"}


def parse_arcgis_survey():
    """arcgis.md 表格 -> {func: {toolbox, judgment, deprecated}}。
    判断取每行第一个以 core/extension/defer 开头的单元格前缀；同名函数
    多行出现时按 defer > extension > core 的保守口径定级（治理从严）。"""
    lines = open(SURVEY_ARCGIS, encoding="utf-8").read().splitlines()
    rank = {"core": 1, "extension": 2, "defer": 3}
    toolbox = None
    seen = {}
    for line in lines:
        m = re.match(r"^## (.+?) toolbox（", line)
        if m:
            toolbox = m.group(1)
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        jud = None
        for c in cells:
            jm = re.match(r"^(core|extension|defer)(?:[：:（(、\s]|$)", c)
            if jm:
                jud = jm.group(1)
                break
        if not jud:
            continue
        deprecated = ("已弃用" in line) or ("退役" in line) \
            or ("deprecated" in line.lower())
        for fn in GP_FN_RE.findall(line):
            if fn not in seen or rank[jud] > rank[seen[fn]["judgment"]]:
                seen[fn] = {"toolbox": toolbox, "judgment": jud,
                            "deprecated": deprecated}
            elif deprecated:
                seen[fn]["deprecated"] = True
    return seen


def parse_qgis_survey():
    """qgis.md §3 表格 -> [{algorithm_id, title, group, platform_judgment}]。"""
    lines = open(SURVEY_QGIS, encoding="utf-8").read().splitlines()
    group = None
    rows = []
    for line in lines:
        m = re.match(r"^#### (.+?)（\d+ 条）", line)
        if m:
            group = m.group(1)
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 5 and re.match(
                    r"^(native|qgis|gdal|pdal|3d):[\w]+$", cells[2]):
                rows.append({"algorithm_id": cells[2], "title": cells[0],
                             "group": group, "platform_judgment": cells[4]})
    return rows


# =====================================================================
# 第五部分：校验与生成
# =====================================================================

def catalog_native_tools():
    spec = importlib.util.spec_from_file_location("catalog_server",
                                                  CATALOG_SERVER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(mod.TOOLS)


def iter_mappings(mapping):
    """展开一条后端映射（含 variants / V32 的 check+repair 双子映射）。"""
    if "variants" in mapping:
        for sub in mapping["variants"].values():
            yield sub
    elif "check" in mapping:
        yield mapping["check"]
        yield mapping["repair"]
    else:
        yield mapping


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    native = {}
    for p in manifest["packages"]:
        if p["package"] in PKG.values():
            native[p["package"]] = {t["name"]: t for t in p["tools"]}
    native["catalog"] = catalog_native_tools()
    native["gdal"] = GDAL_TOOLS
    native["qgis-cli"] = QGIS_CLI_TOOLS
    native["iserver"] = ISERVER_TOOLS
    pkg_of = dict(PKG, catalog="catalog")

    def check_native(backend, name, where):
        if name not in native[pkg_of[backend]]:
            src = ("manifest 的 %s 包" % pkg_of[backend]) \
                if backend != "catalog" else "catalog_server.py 的 TOOLS"
            fail("%s -> %s 不在 %s 中" % (where, name, src))

    # ---- 基础映射校验（沿 v0.1） ----
    tools = {}
    for verb, spec in TABLE.items():
        entry = {"semantics": spec["semantics"], "backends": {}}
        for backend in BACKENDS:
            mapping = spec["backends"].get(backend)
            if mapping is None:
                entry["backends"][backend] = {
                    "native": None,
                    "note": "该后端无此能力，网关返回 NOT_SUPPORTED 并说明"
                            "（或按注记本地处理，见 gis_list_maps/qgis）"}
                continue
            names, arg_note = mapping
            if names == []:
                entry["backends"][backend] = {"native": [], "args": arg_note,
                                              "gateway_local": True}
                continue
            for n in names:
                check_native(backend, n, "base %s" % verb)
            entry["backends"][backend] = {"native": names, "args": arg_note}
        tools[verb] = entry

    # ---- GP 注册表 ----
    gp = parse_arcgis_survey()
    counts = {"core": 0, "extension": 0, "defer": 0}
    for e in gp.values():
        counts[e["judgment"]] += 1
    if len(gp) != 1833 or counts != {"core": 803, "extension": 878,
                                     "defer": 152}:
        fail("GP 普查解析计数不符：total=%d counts=%s（期望 1833 / "
             "803/878/152）" % (len(gp), counts))
    destructive = sorted(fn for fn in gp
                         if fn.rsplit(".", 1)[1].startswith("Delete"))
    whitelist_raw = sorted(fn for fn, e in gp.items()
                           if e["toolbox"] in GP_BATCH1_TOOLBOXES
                           and e["judgment"] == "core")
    if len(whitelist_raw) != 243:
        fail("GP 白名单第一批（三箱 core）计数不符：%d（期望 243）"
             % len(whitelist_raw))
    channel_whitelist = [fn for fn in whitelist_raw
                         if fn not in destructive]
    defer_list = sorted(fn for fn, e in gp.items()
                        if e["judgment"] == "defer")
    gp_entries = {}
    for fn, e in sorted(gp.items()):
        gp_entries[fn] = {
            "toolbox": e["toolbox"], "judgment": e["judgment"],
            "batch": 1 if fn in whitelist_raw else None,
            "channel_open": fn in channel_whitelist,
            "level": "R2" if fn in GP_R2_FUNCS else "R1",
            "license_level": None, "requires_extension": None,
            "deprecated": bool(e["deprecated"]),
            "doc_anchor": "3.1" if e["toolbox"] == "Data Management"
                          else "3.4" if e["toolbox"] in GP_DOC_ANCHOR_34
                          else "mixed(3.1-3.7)"}
    gp_registry = {
        "generated_by": "gateway-v02/build_mapping.py（解析 help-survey/arcgis.md）",
        "evidence_level": "离线协议自检（offline protocol self-check only）："
                          "注册表是普查文档的种子账，不是实机校准证据",
        "source": "help-survey/arcgis.md（ArcGIS Pro 3.4 官方文档普查，"
                  "Data Management 分册锚 3.1）",
        "counts": dict(counts, total=len(gp)),
        "whitelist_batch1_toolboxes": list(GP_BATCH1_TOOLBOXES),
        "whitelist_batch1": whitelist_raw,
        "channel_whitelist": channel_whitelist,
        "channel_whitelist_note": "白名单第一批 243 条扣破坏类（Delete*）后"
                                  "的通道实际可调集；破坏类在通道内回 "
                                  "DESTRUCTIVE_BLOCKED，强制走具名动词",
        "defer_blocklist": defer_list,
        "destructive_blocklist": destructive,
        "governance_fields_note": "license_level / requires_extension 为设计 "
                                  "§3.2 要求的透传三字段之二（deprecated 已由"
                                  "普查行文判定填充）；种子阶段前两字段为 "
                                  "null=未补齐，不以 null 冒充已知，补齐前"
                                  "白名单工具的许可面不作可用性承诺",
        "entries": gp_entries,
    }

    # ---- Processing 种子账 ----
    qrows = parse_qgis_survey()
    qc = {"core": 0, "extension": 0, "defer": 0}
    for r in qrows:
        qc[r["platform_judgment"]] += 1
    if len(qrows) != 374 or qc != {"core": 82, "extension": 242,
                                   "defer": 50}:
        fail("QGIS 普查解析计数不符：total=%d counts=%s（期望 374 / "
             "82/242/50）" % (len(qrows), qc))
    # 统一动词 -> Processing 算法的反向索引（mapped_verb 填充）
    alg_to_verb = {}
    for verb, spec in VERBS.items():
        for backend, mapping in spec["backends"].items():
            if backend != "qgis":
                continue
            for sub in iter_mappings(mapping):
                if sub.get("kind") == "processing":
                    alg_to_verb[sub["algorithm"]] = verb
    proc_entries = []
    for r in qrows:
        proc_entries.append({
            "algorithm_id": r["algorithm_id"],
            "provider": r["algorithm_id"].split(":")[0],
            "title": r["title"], "group": r["group"],
            "platform_judgment": r["platform_judgment"],
            "mapped_verb": alg_to_verb.get(r["algorithm_id"]),
            "params_schema": None,
            "status": "seed", "qgis_version": "3.40"})
    hard_block = []
    for r in qrows:
        aid = r["algorithm_id"]
        reasons = []
        if r["platform_judgment"] == "defer":
            reasons.append("普查判 defer")
        if "executesql" in aid:
            reasons.append("设计 §3.1 点名：裸 SQL 不走 Processing 面")
        if aid in ("gdal:rasterize_over", "gdal:rasterize_over_fixed_value"):
            reasons.append("设计 §3.1 点名：原地覆写类")
        if reasons:
            hard_block.append({"algorithm_id": aid,
                               "reason": "；".join(sorted(set(reasons)))})
    processing_registry = {
        "generated_by": "gateway-v02/build_mapping.py（解析 help-survey/qgis.md）",
        "evidence_level": "离线协议自检：种子账（seed），真源为实机枚举"
                          "（决策 D6）；参数模式待桥侧 algorithmHelp 建账",
        "source": "help-survey/qgis.md（QGIS 3.40 官方文档普查）",
        "counts": dict(qc, total=len(qrows)),
        "entries": proc_entries,
        "hard_blocklist": hard_block,
        "hard_blocklist_note": "网关在 gis_run_processing / 具名动词的 "
                               "Processing 映射执行前硬拦截，回 DEFER_BLOCKED",
    }
    proc_ids = {r["algorithm_id"] for r in qrows}

    # ---- 40 动词校验 ----
    if len(VERBS) != 40 or set(VERBS) != set(VERB_ORDER):
        fail("VERBS 与 VERB_ORDER 不一致或不为 40 个：%d" % len(VERBS))
    mock_tools = {b: set() for b in BACKENDS}
    for verb, spec in TABLE.items():
        for backend in BACKENDS:
            m = spec["backends"].get(backend)
            if m and m[0]:
                mock_tools[backend].update(m[0])
    for verb, spec in VERBS.items():
        for backend, mapping in spec["backends"].items():
            for sub in iter_mappings(mapping):
                st, kind = sub.get("status"), sub.get("kind")
                if st == "ok" and kind == "native":
                    name = sub["native"]
                    if sub.get("bridge_tool_status") == "existing":
                        check_native(backend, name, "%s" % verb)
                    mock_tools[backend].add(name)
                elif st == "ok" and kind == "processing":
                    if sub["algorithm"] not in proc_ids:
                        fail("%s -> 算法 %s 不在 QGIS 普查种子账中"
                             % (verb, sub["algorithm"]))
                    mock_tools["qgis"].add("qgis_run_processing")
                elif st == "ok" and kind == "gp_named":
                    if sub["func"] not in gp:
                        fail("%s -> GP 函数 %s 不在 ArcGIS 普查解析中"
                             % (verb, sub["func"]))
                    mock_tools["arcgis-pro"].add("arcgis_run_gp")
                elif st == "ok" and kind == "template":
                    if sub["template"] not in TEMPLATE_BY_ID:
                        fail("%s -> 模板 %s 不在模板集中"
                             % (verb, sub["template"]))
                    mock_tools["postgis"].add("postgis_exec_template")
                elif st == "ok" and kind in ("gp_channel",
                                             "processing_channel"):
                    mock_tools[backend].add(sub["native"])
    # R3 预检探针工具（网关内置，见 gateway.py PREFLIGHT_PROBES）
    mock_tools["postgis"].update(["postgis_table_summary",
                                  "postgis_table_columns"])
    mock_tools["arcgis-pro"].add("arcgis_list_tables")
    mock_tools["qgis"].add("qgis_list_fields")

    # ---- SuperMap 登记表（V03 用，文件登记非运行时枚举） ----
    sm_entries = []
    for verb in VERB_ORDER:
        mapping = VERBS[verb]["backends"].get("supermap")
        if not mapping:
            continue
        for sub in iter_mappings(mapping):
            if sub.get("wheel"):
                sm_entries.append({"wheel": sub["wheel"], "verb": verb,
                                   "status": sub["status"],
                                   "note": sub.get("note")})
    supermap_registry = {
        "evidence_level": "文件登记（设计 §2 V03：本波为文件登记，非运行时枚举）",
        "source": "UPGRADE-DESIGN-V02.md §2 的 SuperMap 映射行（iobjectspy 10.1.0 口径，D1）",
        "entries": sm_entries,
    }

    # ---- supported_verbs 汇出（基础动词按映射 + 第一波按 ok 子映射） ----
    for b in BACKENDS:
        sv = []
        for verb, spec in TABLE.items():
            m = spec["backends"].get(b)
            if verb == "gis_list_maps" and b == "qgis":
                sv.append(verb)
                continue
            if m and m[0] is not None:
                sv.append(verb)
        for verb in VERB_ORDER:
            m = VERBS[verb]["backends"].get(b)
            if m and any(s.get("status") == "ok"
                         for s in iter_mappings(m)):
                sv.append(verb)
        BACKEND_META[b]["supported_verbs"] = sv

    catalog_evidence = None
    if os.path.exists(CATALOG_INDEX):
        with open(CATALOG_INDEX, encoding="utf-8") as f:
            catalog_evidence = json.load(f).get("evidence_level")

    mapping_out = {
        "generated_by": "gateway-v02/build_mapping.py",
        "sources": [
            "~/workspace/dsh-skills/gis-agent-bridges/manifest/tools-manifest.json",
            "~/workspace/gis-platform-integration/UPGRADE-DESIGN-V02.md",
            "~/workspace/gis-platform-integration/help-survey/arcgis.md",
            "~/workspace/gis-platform-integration/help-survey/qgis.md",
            "~/workspace/gis-platform-integration/data-catalog/catalog_server.py",
        ],
        "evidence_level": "离线协议自检（offline protocol self-check only）。"
                          "本表只证明工具面对得上，不是实机校准证据。",
        "manifest_scope_note": manifest["scope_note"],
        "catalog_evidence_level": catalog_evidence,
        "not_supported_policy": "统一工具面 = 基础 8 动词 + 第一波 40 动词"
                                "（verbs.json）。未列名调用一律 NOT_SUPPORTED；"
                                "设计标待验的映射回 UNVERIFIED_MAPPING；"
                                "defer/破坏类在总通道内硬拦截。不静默降级。",
        "object_model_v02": OBJECT_MODEL_V02,
        "tools": tools,
        "backends": BACKEND_META,
    }
    with open(os.path.join(HERE, "mapping.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(mapping_out, f, ensure_ascii=False, indent=2)

    verbs_out = {
        "generated_by": "gateway-v02/build_mapping.py（规格源为本文件 VERBS）",
        "design_ref": "UPGRADE-DESIGN-V02.md §2（V01–V40）/ §4（确认门）",
        "evidence_level": "离线协议自检：翻译与治理逻辑可由 mock 验证；"
                          "标 pending 的桥侧执行工具未实现前实机不可用",
        "verb_order": VERB_ORDER,
        "verbs": VERBS,
        "supermap_registry": supermap_registry,
    }
    with open(os.path.join(HERE, "verbs.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(verbs_out, f, ensure_ascii=False, indent=2)

    with open(os.path.join(HERE, "gp_registry.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(gp_registry, f, ensure_ascii=False, indent=2)
    with open(os.path.join(HERE, "processing_registry.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(processing_registry, f, ensure_ascii=False, indent=2)

    templates_out = {
        "generated_by": "gateway-v02/build_mapping.py（规格源为本文件 TEMPLATES）",
        "policy": "参数化模板，永不裸 SQL：值走 %(name)s 绑定参数；标识符"
                  "过正则白名单；枚举走封闭集合；平台不开 gis_run_sql 类动词",
        "native_executor": "postgis_exec_template（桥侧待实现 pending；"
                           "网关把渲染后的 sql+params 交桥侧以绑定参数执行）",
        "templates": TEMPLATES,
    }
    with open(os.path.join(HERE, "postgis_templates.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(templates_out, f, ensure_ascii=False, indent=1)

    with open(os.path.join(HERE, "mock_tools.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump({b: sorted(s) for b, s in mock_tools.items()},
                  f, ensure_ascii=False, indent=2)

    print("wrote mapping.json / verbs.json / gp_registry.json / "
          "processing_registry.json / postgis_templates.json / "
          "mock_tools.json")
    print("GP: total=%d core=%d extension=%d defer=%d whitelist_raw=%d "
          "channel_whitelist=%d destructive=%d"
          % (len(gp), counts["core"], counts["extension"],
             counts["defer"], len(whitelist_raw),
             len(channel_whitelist), len(destructive)))
    print("Processing seed: total=%d core=%d extension=%d defer=%d "
          "hard_block=%d" % (len(qrows), qc["core"], qc["extension"],
                             qc["defer"], len(hard_block)))
    print("verbs=40 templates=%d supermap_registry_entries=%d"
          % (len(TEMPLATES), len(sm_entries)))


if __name__ == "__main__":
    main()
