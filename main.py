def find_ancestors(evidence, graph, graph2):
    is_ancestor = [False] * len(graph)
    ancestors = []
    for i in range(len(evidence)):
        if evidence[i] != -1:
            ancestors.append(i)
    while len(ancestors) != 0:
        ancestor = ancestors.pop()
        if not is_ancestor[ancestor]:
            is_ancestor[ancestor] = True
            ancestors = ancestors + graph2[ancestor]
    return is_ancestor


def find_dependence(graph, graph2, is_ancestor, evidence, node1, node2):
    path = [[node1, True]]
    dependent_nodes = [False] * len(graph)
    visited = [False] * (2 * len(graph))
    while len(path) != 0:
        node, direction = path.pop()
        if direction:
            visited_index = node + len(graph)
        else:
            visited_index = node
        if not visited[visited_index]:
            visited[visited_index] = True
            if evidence[node] == -1:
                dependent_nodes[node] = True
            else:
                dependent_nodes[node] = False
            if direction and evidence[node] == -1:
                for k in graph2[node]:
                    path.append([k, True])
                for k in graph[node]:
                    path.append([k, False])
            if not direction:
                if evidence[node] == -1:
                    for k in graph[node]:
                        path.append([k, False])
                if is_ancestor[node]:
                    for k in graph2[node]:
                        path.append([k, True])
    return dependent_nodes[node2]


def mult(cpt1, cpt2):
    cpt = []
    keys1 = cpt1[0].keys()
    keys2 = cpt2[0].keys()
    share_keys = []
    not_share_keys = []
    for key in keys1:
        if key in keys2 and key != 'Prob':
            share_keys.append(key)
        else:
            not_share_keys.append(key)
    for row1 in cpt1:
        for row2 in cpt2:
            flag = 1
            for key in share_keys:
                if row1[key] != row2[key]:
                    flag = 0
            if flag == 0:
                continue
            new_row = row2.copy()
            for key in not_share_keys:
                if key != 'Prob':
                    new_row[key] = row1[key]
                else:
                    new_row['Prob'] = row1['Prob'] * row2['Prob']
            cpt.append(new_row)
    return cpt


def find_joint(probability):
    cpt = probability[0]
    for i in range(1, len(probability)):
        cpt = mult(cpt, probability[i])
    return cpt


def elimination(joint, node):
    del_cpt = []
    id_tracker = {}
    for row2 in joint:
        row = row2.copy()
        id_string = ""
        for key in row.keys():
            if key == node or key == "Prob":
                continue
            if row[key]:
                id_string += "T"
            else:
                id_string += "F"
        if id_string in id_tracker.keys():
            id_tracker[id_string]['Prob'] += row['Prob']
        else:
            id_tracker[id_string] = row
    for key in id_tracker.keys():
        row = id_tracker[key]
        del row[node]
        del_cpt.append(row.copy())
    return del_cpt


def variable_elimination(evidence, node, node2, probability):
    new_probability = probability
    for i in range(len(probability)):
        if i == node or i == node2 or evidence[i] != -1:
            continue
        after_joint_prob = []
        joint_prob = []
        for cpt in new_probability:
            if i in cpt[0].keys():
                joint_prob.append(cpt)
            else:
                after_joint_prob.append(cpt)
        joint = find_joint(joint_prob)
        new_probability = after_joint_prob
        new_probability.append(elimination(joint, i))
    after_joint_prob = []
    joint_prob = []
    for cpt in new_probability:
        if node2 in cpt[0].keys():
            joint_prob.append(cpt)
        else:
            after_joint_prob.append(cpt)
    joint = find_joint(joint_prob)
    new_probability2 = after_joint_prob
    new_probability2.append(elimination(joint, node2))
    final_joint = find_joint(new_probability2)
    if final_joint[0][node]:
        print(round(final_joint[0]['Prob'] / (final_joint[1]['Prob'] + final_joint[0]['Prob']), 2))
    else:
        print(round(final_joint[1]['Prob'] / (final_joint[1]['Prob'] + final_joint[0]['Prob']), 2))
    after_joint_prob = []
    joint_prob = []
    for cpt in new_probability:
        if node in cpt[0].keys():
            joint_prob.append(cpt)
        else:
            after_joint_prob.append(cpt)
    joint = find_joint(joint_prob)
    new_probability = after_joint_prob
    new_probability.append(elimination(joint, node))
    final_joint = find_joint(new_probability)
    if final_joint[0][node2]:
        print(round(final_joint[0]['Prob'] / (final_joint[1]['Prob'] + final_joint[0]['Prob']), 2))
    else:
        print(round(final_joint[1]['Prob'] / (final_joint[1]['Prob'] + final_joint[0]['Prob']), 2))


n = int(input())
graph1 = []
graph2 = []
graph3 = []
probability = []
evidence = [-1] * n
for i in range(n):
    graph1.append([])
    graph2.append([])
    graph3.append([])
for i in range(n):
    input_data = input()
    if input_data == '':
        data = []
    else:
        data = [int(x) for x in input_data.split(" ")]
    for j in data:
        graph1[j - 1].append(i)
        graph2[i].append(j - 1)
        graph2[j - 1].append(i)
        graph3[i].append(j - 1)
    data.reverse()
    prob = [float(x) for x in input().split(" ")]
    cpt = []
    for j in range(2 ** (len(data) + 1)):
        row = {}
        num = bin(j).replace("0b", "")
        for k in range(len(data)):
            if len(num) <= k or num[len(num) - k - 1] == "0":
                row[data[k] - 1] = True
            else:
                row[data[k] - 1] = False
        if j < len(prob):
            row[i] = True
            row['Prob'] = prob[j]
        else:
            row[i] = False
            row['Prob'] = 1 - prob[j - len(prob)]
        cpt.append(row)
    probability.append(cpt)
data = list(input().split(","))
for i in data:
    if i[1] == '-':
        evidence[int(i[0]) - 1] = bool(int(i[3]))
    else:
        evidence[int(i[0] + i[1]) - 1] = bool(int(i[4]))
node1, node2 = [int(x) for x in input().split(" ")]
new_probability = []
for i in range(len(probability)):
    cpt = []
    for row in probability[i]:
        if row[i] != evidence[i] and evidence[i] != -1:
            continue
        flag = 1
        for j in graph3[i]:
            if row[j] != evidence[j] and evidence[j] != -1:
                flag = 0
        if flag:
            cpt.append(row)
    new_probability.append(cpt)
ancestor = find_ancestors(evidence, graph1, graph3)
flag = find_dependence(graph1, graph3, ancestor, evidence, node1 - 1, node2 - 1)
if flag:
    print("dependent")
else:
    print("independent")
variable_elimination(evidence.copy(), node1 - 1, node2 - 1, new_probability.copy())
