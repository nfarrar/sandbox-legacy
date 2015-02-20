#/usr/bin/env python

import logging
import os
import re
import sys

BASE = os.path.join(os.environ['HOME'], '.syslog')

from syslogtools.dataimporter import ZipImporter
from syslogtools.flowmodels import Flow, FlowList

sys.path.append(os.path.join(BASE_PATH, 'tools'))

# Setup paths. 
ARCHIVES = os.path.join(BASE, 'archives')
DATA = os.path.join(BASE, 'client/data')
REPORT = os.path.join(BASE, 'client/reports')
CACHE = os.path.join(BASE, 'client/.cache')


def get_collection_list():
    l = []
    for dir in os.listdir(BASE):
        l.append(dir.strip('/'))
    return l

def build_flow(line):
    """
    Build a flow object from a syslog entry.

    Args:
        - line: A syslog entry. Specific to ASA. Using the format:
          id protocol sinterface saddress sport dinterface daddress dport
    """

    junk = r'.*?'
    syslog_id = r'(106100)'
    protocol = r'(tcp|udp)'
    interface = r'(pci_inside|pci_outside|pci-npci_dmz)'
    ip_address = r'((?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}))'
    port = r'([\d]{1,5})'

    asa_106100 = junk + syslog_id + junk + protocol + junk +\
        interface + r'//?' + ip_address + r'\(' + port + r'\).*?' +\
        interface + r'//?' + ip_address + r'\(' + port + r'\)'

    match = re.search(asa_106100, line)

    try:
        parts = re.search(asa_106100, line).groups()
        f = Flow(parts[3], parts[6], parts[7], parts[1])
        f['ingress'] = parts[2]
        f['egress'] = parts[5]
        return f
    except:
        return None


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    # Serialize the data so we can quckly reload it without reparsing. 
    collections = get_collection_list()
    for collection in collections:
        raw_data = ZipImporter(os.path.join(ARCHIVE, collection)).subset(0,20)
        fl = FlowList()
        for line in raw_data:
            try:
                fl.insert(build_flow(line))
            except:
                pass
        logging.info('built flowlist from ' + collection + ' of length ' + str(len(fl)))
        fl.save(BASE + collection + CACHE + 'all.pk')


def process_collection(collection):
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    path_suffix = "compressed_data/"
    importer = dataimporter.ZipImporter(path_base + collection + path_suffix)
    #subset = importer.subset(0,200)
    outside = flowmodels.FlowList()
    dmz = flowmodels.FlowList()
    parser = logparsers.ASASyslogParser()

    interface_matrix = { }
    num_parse_good = 0
    num_parse_fail = 0

    #for line in subset:
    for line in importer:
        parts = parser.parse(line)
        if parts == None:
            num_parse_fail = num_parse_fail + 1
        else:
            # 0     1           2           3   4       5           6   7
            # id    protocol    interface   ip  port    interface   ip  port
            if (parts[2], parts[5]) not in interface_matrix.keys():
                interface_matrix[parts[2], parts[5]] = 1
            else:
                interface_matrix[parts[2], parts[5]] = interface_matrix[parts[2], parts[5]] + 1

            if parts[2] == 'pci_outside' and parts[5] == 'pci_inside':
                outside.add_flow(flowmodels.Flow(parts[3], parts[6], parts[7], parts[1]))
            elif parts[2] == 'pci-npci_dmz' and parts[5] == 'pci_inside':
                #print 'dmz: ' + str(parts)
                dmz.add_flow(flowmodels.Flow(parts[3], parts[6], parts[7], parts[1]))

    flowmodels.FlowList.save(outside, 'serialized/' + collection.strip('/') + '_outside.obj')
    flowmodels.FlowList.save(dmz, 'serialized/' + collection.strip('/') + '_dmz.obj')

    report = open('reports/' + collection.strip('/') + '.txt', 'w')
    report.write("Collection:\t\t" + collection.strip('/') + "\n\n")
    report.write( "Archives Read:\t\t" + str(importer.num_archives) + "\n")
    report.write("Files Read:\t\t" + str(importer.num_files) + "\n")
    report.write("Lines Read:\t\t" + str(importer.num_lines) + "\n\n")

    report.write("Lines Parsed:\t\t" + str(num_parse_good) + "\n")
    report.write("Lines Not Parsed:\t" + str(num_parse_fail) + "\n\n")

    report.write("Results of Interface Matrix ...\n")
    for key in interface_matrix.keys():
        report.write(key[0] + "\t->\t" + key[1] + "\t" + str(interface_matrix[key]) + "\n")
    report.write("\n\n")

    report.write("Results of Flow Generation ...\n")
    report.write("Outside, Unique:\t" + str(outside.unique) + "\n")
    report.write("Outside, Nonunique:\t" + str(outside.total) + "\n\n")

    report.write("DMZ, Unique:\t\t" + str(dmz.unique) + "\n")
    report.write("DMZ, Nonunique:\t\t" + str(dmz.total) + "\n")
    report.close()

def compare_collections():

    outside_suffix = '_outside.obj'
    dmz_suffix = '_dmz.obj'

    collections = []

    # collections.append("2011.07.03-2011.07.11")
    # collections.append("2011.07.12-2011.07.17")
    # collections.append("2011.07.18-2011.07.27")
    # collections.append("2011.07.28-2011.08.10")
    # collections.append("2011.08.11-2011.08.28")

    outside_all_standard = flowmodels.FlowList()
    outside_all_nonstandard = flowmodels.FlowList()
    dmz_all_standard = flowmodels.FlowList()
    dmz_all_nonstandard = flowmodels.FlowList()

    for collection in collections:

        #    1. load collection into memory
        #    2. separate into standard & nonstandard lists (port < 1025)
        #    3. separate into new & old lists
        #    4. write report
        #    5. add new standard flows into previous flows

        # 1. load collection into memory
        outside_base = flowmodels.FlowList.load(path_base + collection + '_outside.obj')
        outside_standard = flowmodels.FlowList()
        outside_nonstandard = flowmodels.FlowList()
        outside_standard_new = flowmodels.FlowList()
        outside_standard_old = flowmodels.FlowList()
        outside_nonstandard_new = flowmodels.FlowList()
        outside_nonstandard_old = flowmodels.FlowList()

        dmz_base = flowmodels.FlowList.load(path_base + collection + '_dmz.obj')
        dmz_standard = flowmodels.FlowList()
        dmz_nonstandard = flowmodels.FlowList()
        dmz_standard_new = flowmodels.FlowList()
        dmz_standard_old = flowmodels.FlowList()
        dmz_nonstandard_new = flowmodels.FlowList()
        dmz_nonstandard_old = flowmodels.FlowList()

        # 2. separate into standard and nonstandard lists
        for flow_key in outside_base.keys():
            if int(outside_base[flow_key].destination_port) < int(1025):
                outside_standard.add_flow(outside_base[flow_key])
            else:
                outside_nonstandard.add_flow(outside_base[flow_key])

        for flow_key in dmz_base.keys():
            if int(dmz_base[flow_key].destination_port) < int(1025):
                dmz_standard.add_flow(dmz_base[flow_key])
            else:
                dmz_nonstandard.add_flow(dmz_base[flow_key])

        # 3. separate into new & old lists
        for flow_key in outside_standard.keys():
            if flow_key not in outside_all_standard.keys():
                outside_standard_new.add_flow(outside_standard[flow_key])
            else:
                outside_standard_old.add_flow(outside_standard[flow_key])

        for flow_key in outside_nonstandard.keys():
            if flow_key not in outside_all_nonstandard.keys():
                outside_nonstandard_new.add_flow(outside_nonstandard[flow_key])
            else:
                outside_nonstandard_old.add_flow(outside_nonstandard[flow_key])

        for flow_key in dmz_standard.keys():
            if flow_key not in dmz_all_standard.keys():
                dmz_standard_new.add_flow(dmz_standard[flow_key])
            else:
                dmz_standard_old.add_flow(dmz_standard[flow_key])

        for flow_key in dmz_nonstandard.keys():
            if flow_key not in dmz_all_nonstandard.keys():
                dmz_nonstandard_new.add_flow(dmz_nonstandard[flow_key])
            else:
                dmz_nonstandard_old.add_flow(dmz_nonstandard[flow_key])

        # 4. writing reports
        try:
            file = open('/home/oxseyn/Documents/syslogtools/clients/reports/compare/' + collection + '_outside.txt', 'w')
            file.write('outside:\t\t' + collection +'\n')
            file.write('previous standard:\t' + str(outside_all_standard.unique) + '\n')
            file.write('previous nonstandard:\t' + str(outside_all_nonstandard.unique) + '\n')
            file.write('base:\t\t\t' + str(outside_base.unique) + '\n')
            file.write('standard:\t\t' + str(outside_standard.unique) + '\n')
            file.write('standard new:\t\t' + str(outside_standard_new.unique) + '\n')
            file.write('standard old:\t\t' + str(outside_standard_old.unique) + '\n')
            file.write('nonstandard:\t\t' + str(outside_nonstandard.unique) + '\n')
            file.write('nonstandard new:\t' + str(outside_nonstandard_new.unique) + '\n')
            file.write('nonstandard old:\t' + str(outside_nonstandard_old.unique) + '\n')
            logging.info('wrote report')
            file.close()
        except:
            logging.info('failed to save report')

        try:
            file = open(BASE + '/reports/' + collection + '_dmz.txt', 'w')
            file.write('dmz:\t\t' + collection +'\n')
            file.write('previous standard:\t' + str(dmz_all_standard.unique) + '\n')
            file.write('previous nonstandard:\t' + str(dmz_all_nonstandard.unique) + '\n')
            file.write('base:\t\t\t' + str(dmz_base.unique) + '\n')
            file.write('standard:\t\t' + str(dmz_standard.unique) + '\n')
            file.write('standard new:\t\t' + str(dmz_standard_new.unique) + '\n')
            file.write('standard old:\t\t' + str(dmz_standard_old.unique) + '\n')
            file.write('nonstandard:\t\t' + str(dmz_nonstandard.unique) + '\n')
            file.write('nonstandard new:\t' + str(dmz_nonstandard_new.unique) + '\n')
            file.write('nonstandard old:\t' + str(dmz_nonstandard_old.unique) + '\n')
            logging.info('wrote report')
            file.close()
        except:
            logging.info('failed to save report')

        # 5. add new flows to totals
        for flow_key in outside_standard_new.keys():
            outside_all_standard.add_flow(outside_standard_new[flow_key])

        for flow_key in outside_nonstandard_new.keys():
            outside_all_nonstandard.add_flow(outside_nonstandard_new[flow_key])

        for flow_key in dmz_standard_new.keys():
            dmz_all_standard.add_flow(dmz_standard_new[flow_key])

        for flow_key in dmz_nonstandard_new.keys():
            dmz_all_nonstandard.add_flow(dmz_nonstandard_new[flow_key])

    try:
        count = 0
        outside_rule_file = open(BASE + 'client/reports/outside.txt', 'w')
        for flow_key in outside_all_standard.keys():
            rule = rulesetgenerator.ASARulesetGenerator.rule(count + 'pci_outside' + outside_all_standard[flow_key])
            count = count + 1
            for line in rule:
                outside_rule_file.write(line + '\n')
            outside_rule_file.write('\n')
            outside_rule_file.close()
        logging.info('wrote ' + str(count) + ' rules')
    except:
        logging.info('failed to write rulesets')

    try:
        outside_manual_file = open(BASE + '/clients/reports/nonstandard_flows/outside.txt', 'w')
        for flow_key in outside_all_nonstandard.keys():
            outside_manual_file.write(str(outside_all_nonstandard[flow_key]) + '\n')
        outside_manual_file.close()
        logging.info('wrote nonstandard flows')
    except:
        logging.info('failed to write nonstandard flows')

    try:
        count = 0
        dmz_rule_file = open(BASE + '/clients/rules/dmz.txt', 'w')
        for flow_key in dmz_all_standard.keys():
            rule = rulesetgenerator.ASARulesetGenerator.rule(count + 'pci-npci_dmz' + dmz_all_standard[flow_key])
            count = count + 1
            for line in rule:
                dmz_rule_file.write(line + '\n')
            dmz_rule_file.write('\n')
            dmz_rule_file.close()
        logging.info('wrote ' + str(count) + 'rules.')
    except:
        logging.info('failed to write rulesets')

    try:
        dmz_manual_file = open(BASE + '/clients/reports/nonstandard_flows/dmz.txt', 'w')
        for flow_key in dmz_all_nonstandard.keys():
            dmz_manual_file.write(str(dmz_all_nonstandard[flow_key]) + '\n')
        dmz_manual_file.close()
        logging.info('failed to write nonstandard flows')
    except:
        logging.info('failed to write nonstandard flows')
