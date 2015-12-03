import re

def remove_comments(html_string):
    return re.sub(r'<!--.*?-->', '', html_string)

def remove_scripts(html_string):
    return re.sub(r'<script>.*?</script>', '', html_string)

def split(html_string):
    return re.findall(r'(</.+?>)|(<.+?>)|(.*?(?=<))', html_string)

def is_self_closing(node_string):
    print(node_string)
    return bool(re.match(r'<(area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|source|track|wbr)\s?', node_string))

def make_DOM_from_HTMLstring(html_string):
    html_string = remove_comments(html_string)
    html_string = remove_scripts(html_string)
    html_parts = split(html_string)
    return DOM(html_parts)

class DOM:
    def __init__(self, html_parts):
        self.head = html_parts[0][1]
        self.type = self.get_type(self.head)
        self.inner_nodes = 0 #defaults
        self.children = [] #defaults
        if self.type and not is_self_closing(self.head):
            self.id = self.get_id(self.head)
            self.classes = self.get_classes(self.head)
            self.innerHTML = self.get_innerHTML(html_parts)
            if self.inner_nodes > 0:
                self.get_children(html_parts)

    def get_innerHTML(self, html_parts):
        print("html parts:")
        print(html_parts)
        current_index = 1
        depth = 1
        innerHTML = ""
        safe_check = 0 # remove after testing
        failsafe = 100 # remove aafter testing
        while depth > 0 and safe_check < failsafe:
            self.inner_nodes += 1
            t = html_parts[current_index]
            print(t)
            innerHTML += t[0] + t[1] + t[2]
            if t[1] and not is_self_closing(t[1]):
                if t[1]:
                    depth += 1
                if t[0]:
                    depth -= 1
            safe_check += 1 # remove after testing
        return innerHTML

    def get_type(self, html_part):
        r = re.search(r'<(\w+)\s?', html_part)
        if r:
            return r.group(1) or ""
        return ""


    def get_classes(self, html_part):
        r = re.search(r'class=[\"\'](.*?)[\"\']', html_part)
        if r and r.group(1):
            return r.group(1).split(" ")
        else:
            return []

    def get_id(self, html_part):
        r = re.search(r'id=[\"\'](.*?)[\"\']', html_part)
        if r:
            return r.group(1) or ""
        return ""

    def get_children(self, html_parts):
        sum_of_child_lengths = 0
        current_child_index = 1
        while sum_of_child_lengths < self.inner_nodes:
            current_child = DOM(html_parts[current_child_index:])
            self.children.append(current_child)
            current_child_index += current_child.inner_nodes


print(make_DOM_from_HTMLstring("<div><div></div><div></div></div>").children)





