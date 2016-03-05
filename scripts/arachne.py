#!/usr/bin/python3

def _RecurFind(node,creator,List):
    try:
        [List.append(x) for x in node.children[creator.name]]
    except:
        pass
    [_RecurFind(x,creator,List) for x in node.allchildren(ReturnList=True)]
    
class NodeList(list):
    def __xor__(self,other):
        t=NodeList([])
        for el in self+other:
            if (el in self and el not in other) or (el not in self and el in other) and el not in t:
                t.append(el)
        return t
    def __and__(self,other):
        t=NodeList([])
        for el in self+other:
            if el in self and el in other and el not in t:
                t.append(el)
        return t
    def __or__(self,other):
        t=NodeList([])
        for el in self+other:
            if el not in t:
                t.append(el)
        return t
    
    def __neg__(self):
        return NodeList([-x for x in self])

    def __pos__(self):
        return NodeList([+x for x in self])

    def __gt__(self,other):
        return NodeList([x>other for x in self])

    def __lt__(self,other):
        return NodeList([x<other for x in self])

    def __rshift__(self,other):
        return NodeList([x>>other for x in self])

    def __lshift__(self,other):
        return NodeList([x<<other for x in self])
    
        
def StrictMatch(Other,Self):
    if type(Self) is not list:
        return Other == Self
    elif type(Self) is list:
        return Other in Self
    else:
        return False
        
def FuzzyMatch(Other,Self):
    if Other.find(Self) > -1 or Self.find(Other) > -1:
        return True
    else:
        return False

def RegexMatch(Other,Self):
    import re
    if re.search(Other,Self) is not None:
        return True
    return False
        
class Node:
    def __init__(self,ParentNode=0,NodeCreator=False,Content=b"root",**kargs):        
        self.content = Content
        try:
            self.name    = self.content.decode('utf-8')
        except:
            self.name    = self.content
        self.children = {}
        self.parent = ParentNode
        self.creator = NodeCreator
        
    def __gt__(self,other):
        if type(other) is not tuple:
           return self.childby(other)
        else:
           return self.childby(other[0])[other[1]]
                 
    def __lt__(self,other):
        if type(other) is not tuple:
           return self.parent.childby(other)
        else:
           return self.parent.childby(other[0])[other[1]]

    def __rshift__(self,other):
        return self.descendant(other)

    def __lshift__(self,other):
        return self.ancestor(other)
    
    def __neg__(self):
        return self.content

    def __pos__(self):
        try:
            return self.name
        except:
            return self.content
        
    def __add__(self,other):
         if type(other) is tuple:
            return [self.newchildren(x) for x in other]
         else:
            return self.newchildren(other)

    def __getitem__(self,index):
        return self.content[index]

    def newchildren(self,Creator,*args,**kargs):
        new_children=Creator.transform(self,*args,**kargs)
        if not new_children:
            return False

        cName = Creator.name 
        if cName in self.children:
            self.children[cName] += new_children
        else:
            self.children[cName]   = new_children 

        return new_children if len(new_children) >= 1 and 'ReturnList' in kargs else new_children[0]

    def has_content(self,search_content,**kargs):
        IsMatch   = False
        ParseIt   = False if 'ParseIt' not in kargs else kargs['ParseIt']
        ByName    = False if 'ByName'  not in kargs else kargs['ByName']
        ExcludeIt = False if 'ExcludeIt' not in kargs   else kargs['ExcludeIt']
        Compare  = FuzzyMatch if 'Matching' not in kargs else kargs['Matching']

        if ParseIt:
            kargs.pop('ParseIt')
        if type(search_content) is int:
            Compare=StrictMatch
            
        if ParseIt is not False:
            from modules import parse_bytes
            P = parse_bytes()
        search_content = bytes(search_content,encoding="utf-8") if (ParseIt is False and type(self.content) is bytes and type(search_content) is not bytes) else search_content
        if ParseIt is True:
            IsMatch = Compare(search_content,P.Parse(self.content**kargs))
        elif ByName is True:
            try:
                IsMatch = Compare(search_content,self.name)
            except:
                IsMatch = False
        else:
            IsMatch = Compare(search_content,self.content)

        if IsMatch is True and ExcludeIt is False:
            return True
        elif IsMatch is False and ExcludeIt is True:
            return True
        else:
            return False

    # list of all children created from a specific Creator function

    def createdfrom(self,Creator): 
        try:
            return self.children[Creator.name]
        except KeyError:
            return False
        
    # list of all children created from any Creator function

    def childby(self,Creator,ReturnList=False):
        try:
            createdChildren=self.children[Creator.name]                    
            createdLen=len(createdChildren)
        except KeyError:
            return False
        
        if createdLen > 1 or ReturnList:
            return createdChildren
        else:
            return createdChildren[0]

    def peer(self,Creator):
        return self.parent.childby(Creator)

    def allchildren(self,ReturnList=False):
        allchild=NodeList([])
        [[allchild.append(x) for x in self.children[c]] for c in self.children]
        if len(allchild) > 1:
            return allchild
        elif len(allchild) == 1:
            if ReturnList is False:
                return allchild[0]
            else:
                return allchild
        elif ReturnList is False:
            return False
        else:
            return allchild
    
    # find parent node created by arbitrary Parent or Creator

    def has_parent(self,SearchedForParent):
        ancestor = self
        while ancestor.parent is not None:
            if ancestor.parent is SearchedForParent:
                return ancestor
            ancestor = ancestor.parent
        return False
    
    def ancestor(self,SearchedForCreator):
        ancestor = self.parent
        while ancestor.parent:
            if ancestor.creator is SearchedForCreator or  ancestor.creator.name==SearchedForCreator:
                return ancestor
            ancestor = ancestor.parent
        return False

    # find all child nodes created by arbitrary Creator
    def descendant(self,SearchedForCreator,ReturnList=False):
        descendants = NodeList([])
        _RecurFind(self,SearchedForCreator,descendants)
        if len(descendants) == 1 and ReturnList is False:
            return descendants[0]
        else:
            return descendants

# return list of all children with a particular content

    def add(self,child):
        self.new_children.append(child)
    
    def Root(self):
        try:
            return self.parent.root
        except:
            return self

    root = property(Root)
    
class Creator:
    def __init__(self,function,**kargs):
        self.children       = NodeList([])
        self.transformFunc  = function
        self.name           = str(id(self)) if 'Name' not in kargs else kargs.pop('Name')
        self.init_kargs     = kargs
        
    def __eq__(self,other):
        return self.created_content(other,ReturnList=True)

    def __neg__(self):
        return -self.children

    def __iter__(self):
        return iter(self.children)
    
    def has_children(self):
        if len(self.children) > 0:
            return True
        else:
            return False

    def transform(self,parentNode,*args,**kargs):
        newargs = kargs.copy()
        newargs.update(self.init_kargs)
        newChildren=NodeList([Node(parentNode,self,datum,**kargs) for datum in self.transformFunc(parentNode,*args,**newargs)])
        self.children += newChildren
        return newChildren if len(newChildren) > 0 else False
    
    def created_content(self,content,ReturnList=False,**kargs):
        matches = NodeList([])
        [matches.append(x) if x.has_content(content,**kargs) else None for x in self.children]

        num_matches = len(matches)

        if num_matches < 1:
            return NodeList([])
        elif num_matches == 1 and ReturnList is False:
            return matches[0]
        else:
            return matches
