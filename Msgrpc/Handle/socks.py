# -*- coding: utf-8 -*-
# @File  : socks.py
# @Date  : 2021/2/25
# @Desc  :

from Core.Handle.setting import Settings
from Lib.api import data_return, is_empty_ports
from Lib.configs import CODE_MSG, Socks_MSG, RPC_JOB_API_REQ
from Lib.msfmodule import MSFModule
from Lib.notice import Notice
from Msgrpc.Handle.job import Job


class Socks(object):
    """socks代理"""

    @staticmethod
    def list_msf_socks():
        lhost = Settings.get_lhost()
        socks_list = []
        infos = Job.list_msfrpc_jobs()
        if infos is None:
            return socks_list
        for key in infos.keys():
            info = infos.get(key)
            jobid = int(key)
            if info.get('name') == 'Auxiliary: server/socks4a_api':
                datastore = info.get('datastore')
                if datastore is not None:
                    onesocks4a = {'ID': jobid,
                                  "type": "msf_socks4a",
                                  "lhost": lhost,
                                  "port": datastore.get("SRVPORT"),
                                  'datastore': datastore}
                    socks_list.append(onesocks4a)
            elif info.get('name') == 'Auxiliary: server/socks5_api':
                datastore = info.get('datastore')
                if datastore is not None:
                    onesocks4a = {'ID': jobid,
                                  "type": "msf_socks5",
                                  "lhost": lhost,
                                  "port": datastore.get("SRVPORT"),
                                  'datastore': datastore}
                    socks_list.append(onesocks4a)

        return socks_list

    @staticmethod
    def create(socks_type=None, port=None):
        if socks_type == "msf_socks4a":
            opts = {'SRVHOST': '0.0.0.0', 'SRVPORT': port}
            flag, lportsstr = is_empty_ports(port)
            if flag is not True:
                # 端口已占用
                context = data_return(408, {}, CODE_MSG.get(408))
                return context

            result = MSFModule.run(module_type="auxiliary", mname="server/socks4a_api", opts=opts, runasjob=True,
                                   timeout=RPC_JOB_API_REQ)
            if isinstance(result, dict) is not True or result.get('job_id') is None:
                opts['job_id'] = None
                context = data_return(303, opts, Socks_MSG.get(303))
            else:
                job_id = int(result.get('job_id'))
                if Job.is_msf_job_alive(job_id):
                    opts['job_id'] = int(result.get('job_id'))
                    Notice.send_success(f"新建msf_socks4a代理成功,Port: {opts.get('SRVPORT')}",
                                        f"Create msf_socks4a success,Port: {opts.get('SRVPORT')}")
                    context = data_return(201, opts, Socks_MSG.get(201))
                else:
                    context = data_return(306, opts, Socks_MSG.get(306))
            return context
        elif socks_type == "msf_socks5":
            opts = {'SRVHOST': '0.0.0.0', 'SRVPORT': port}
            flag, lportsstr = is_empty_ports(port)
            if flag is not True:
                # 端口已占用
                context = data_return(408, {}, CODE_MSG.get(408))
                return context

            result = MSFModule.run(module_type="auxiliary", mname="server/socks5_api", opts=opts, runasjob=True,
                                   timeout=RPC_JOB_API_REQ)
            if isinstance(result, dict) is not True or result.get('job_id') is None:
                opts['job_id'] = None
                context = data_return(303, opts, Socks_MSG.get(303))
            else:
                job_id = int(result.get('job_id'))
                if Job.is_msf_job_alive(job_id):
                    opts['job_id'] = int(result.get('job_id'))
                    Notice.send_success(f"新建msf_socks5代理成功,Port: {opts.get('SRVPORT')}",
                                        f"Create msf_socks5 success,Port: {opts.get('SRVPORT')}")
                    context = data_return(201, opts, Socks_MSG.get(201))
                else:
                    context = data_return(306, opts, Socks_MSG.get(306))
            return context

    @staticmethod
    def destory(socks_type=None, jobid=None):
        if socks_type == "msf_socks4a":
            flag = Job.destroy(jobid)
            if flag:
                if Job.is_msf_job_alive(jobid) is not True:
                    Notice.send_success(f"删除msf_socks4a代理 JobID:{jobid}", f"Delete msf_socks4a JobID:{jobid}")
                    context = data_return(204, {}, Socks_MSG.get(204))
                else:
                    context = data_return(304, {}, Socks_MSG.get(304))
            else:
                context = data_return(304, {}, Socks_MSG.get(304))
            return context
        elif socks_type == "msf_socks5":
            flag = Job.destroy(jobid)
            if flag:
                if Job.is_msf_job_alive(jobid) is not True:
                    Notice.send_success(f"删除msf_socks5代理 JobID:{jobid}", f"Delete msf_socks5 JobID:{jobid}")
                    context = data_return(204, {}, Socks_MSG.get(204))
                else:
                    context = data_return(304, {}, Socks_MSG.get(304))
            else:
                context = data_return(304, {}, Socks_MSG.get(404))
            return context
