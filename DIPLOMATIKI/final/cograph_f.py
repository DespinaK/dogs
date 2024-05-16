from copy import deepcopy
import networkx as nx
import matplotlib
from collections import deque
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import scipy as sp
import sys
import tkinter as tk
from tkinter import messagebox
import json



graph={ 0: [2,4],
    1: [2,4],
    2: [0,1, 3, 4],
    3: [2],
    4: [0,1,2]
    }
test={ 0: [2,4,5],
    1: [2,4,5],
    2: [0,1, 3, 4,5],
    3: [2],
    4: [0,1,2,5],
    5:[0,1,2,4]
    }




graph4= {0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [],
    4: []}




S=[]

class createnode:
	def __init__(self,data,id):
		self.root=data
		self.children=[]
		self.id=id

class qt:
	def __init__(self,t):
		self.taf = t
		self.children=[]

class qxt:
	def __init__(self,t):
		self.taf = t
		self.children=[]

	

def read_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        cograph = json.load(file)
    return cograph

def make_g(graph_data):
	g={}
	
	for edge in graph_data["edges"]:
		g[edge["source"]]=edge["target"]
		
	print("here is g", g)
	return(g)

						
def is_cograph(graph):
	c,v =is_g_connected(graph)
	if c:
		if len(graph)<4:
			print("is cograph")
			return True
		for i in graph:
			for j in graph:
				if i!=j:
					for w in graph[j]:
						if w!=i and w!=j and w not in graph[i]:
							for x in graph[w]:
								if i!= x and j!=x and x not in graph[i] and x not in graph[j]:
									
									print("p4 found")
									print("graph",graph)
									return False
		print("is cograph")
		return True
	else: 
		components = split_into_connected(graph,v)
		for g in components:
			component= make_graph_from_comp(graph,g)
			print("comp",component)
			if not is_cograph(component):
				return False
		return True


											



def is_g_connected(graph):
	max=0
	for i in graph:
		if i>max:
			max=i
	visited= [None]*(max+1)
	
	for i in graph:
		visited[i]=False
	nxt= next(iter(graph))
	
	dfs(graph,nxt,visited)
	
	
	flag=0
	for i in visited:
		if i==False:
			flag=1
	if flag==1:
		print("Graph is not connected")
		

		return(False,visited)
		
		
	else:
		print("Graph is connected")
		return(True,visited)

def dfs(*args): 
	if len(args)==3:
		graph=args[0]
		node=args[1]
		visited = args[2]
		visited[node]=True
		for neighbor in graph[node]:
			
			if not visited[neighbor]:
				dfs(graph,neighbor,visited)
	elif len(args)==4:	
		graph=args[0]
		node=args[1]
		visited = args[2]
		component=args[3]	
		visited[node]=True
		component.append(node)

		for neighbor in graph[node]:
			if not visited[neighbor]:
				dfs(graph,neighbor,visited,component)

"""def dfs(graph,node,visited,component):
	visited[node]=True
	component.append(node)

	for neighbor in graph[node]:
		if not visited[neighbor]:
			dfs(graph,neighbor,visited,component)"""

def split_into_connected(graph,visited):

	max=0
	for i in graph:
		if i>max:
			max=i
	visited= [None]*(max+1)
	for i in graph:
		visited[i]=False
	components = []
	
	for node in range(max+1):
		if visited[node] ==False:
			component= []

			dfs(graph,node,visited,component)
			components.append(component)
	
	
	return(components)
	
	

def complement(component):
	
	complement = {vertex: [] for vertex in component}
	for node in component:
		for j in component:
				
			if j not in component[node] and j!=node:
				complement[node].append(j)

				
	
	
	return(complement)



def make_graph_from_comp(graph,component):
	component_graph = {vertex: [] for vertex in component}
	
	for i in component_graph:
		component_graph[i]=graph[i]
	
	return(component_graph)

def make_cotree(graph,node,id=0):
	print("start of make-COTREE, this is the graph:", graph)
	
	connected,visited=is_g_connected(graph)
	
	if len(graph)==1:
		if node.root == graph: #last 
			node.root=next(iter(graph.keys()))
			
			return(0)
		
		node.children.append(createnode(next(iter(graph.keys())),0))
		
		return(0)
	

	if connected==False: #enosi me 1 ta components\
		node.root="0-node"
		
		if len(graph)==2:
			key_it=iter(graph.keys())
			node.children.append(createnode(next(key_it),0))
			

			node.children.append(createnode(next(key_it),0))
			

			
			return(0)
		else:
			

			
			con_components = split_into_connected(graph,visited)
			
		
			for i in range(len(con_components)):
			
				compon_graph=make_graph_from_comp(graph,con_components[i])
				
				if len(compon_graph)==1:
					node.children.append(createnode(compon_graph,0))
				else:
					node.children.append(createnode("1-node",id))
					id+=1
				make_cotree(compon_graph,node.children[-1],id)
			
	elif connected==True: #enosi me 0
		

		node.root="1-node"
		components=None
		complements=complement(graph)
		print("Comp", complements)
		
		con_components = split_into_connected(complements,visited)
		
		
		for i in range(len(con_components)):
		
			compon_graph=make_graph_from_comp(complements,con_components[i])
			print("con components", con_components[i])
			print("Compoin_graph", compon_graph)
			complement_con=complement(compon_graph)
			
			if len(complement_con)==1: #leaf
				node.children.append(createnode(complement_con,0))
			else:
				node.children.append(createnode("0-node",id))
				id+=1

			make_cotree(complement_con,node.children[-1],id)
		

def print_cotree(node,level=0,prefix="Root: "):
	
	if node:
		print("  ")
		print("   "*(level)+ prefix+" :"+str(node.root))
		j=0
		for i in node.children:
			print_cotree(i, level+1,"child of "+str(node.root))

def find_leaves(node,leaves):
	
	if not node.children:
		
		#return leaves
		leaves.append(node.root)
		
		
	else:

		for child in node.children:
			
			find_leaves(child,leaves)
		return leaves
	return leaves
	
		



def CMxCC(node,x,x_neighbours):
	global S
	print("node 1st", node.root)

	if node.root=="1-node":
		
	
		t=[]

		

		for child in node.children:
			leaves=[]
			
			leaves=find_leaves(child,leaves)
			print("child.root 297",child.root)
			#if (child.root!="1-node" and child.root!="0-node"):
				#leaves=[]
			print("leaves 299",leaves)
			
			for neigh in x_neighbours:
				if neigh in leaves:
					if child not in t:
						print("in t")
						t.append(child) #qxr


		
		
		
		if t:
			print("hahah")

			for i in t:
				q=qt(i)
				qx=qxt(i)
				
				for child in i.children:
					q.children.append(child)
				

					leaves=[]
					leaves=find_leaves(child,leaves)
					print("child, leaves:",child.root,leaves)
					#if (child.root!="1-node" and child.root!="0-node"):
						#leaves=[]
					for neigh in x_neighbours:
						if neigh in leaves:
							if child not in qx.children:
								print("in qx", child.root)
								qx.children.append(child)
				if len(qx.children)<len(q.children) and len(qx.children)>0 and len(q.children)>0:
					


					l=[]
					l=find_leaves(q.taf,l)
					#if (q.taf.root!="1-node" and q.taf.root!="0-node"):
						#l=[]
					print("here", q.taf.root)
					
						
					Nx_tomi_Mt= list(set(l) & set(x_neighbours))
					print("intersection",Nx_tomi_Mt)
					#print("l",l )
					#print("xnei", x_neighbours)
					#print("eimai edw")
					rl=[]
					rl=find_leaves(node,rl)
					#if (node.root!="1-node" and node.root!="0-node"):
						#rl=[]
					print("leaves 341",rl)
					Mr_div_Mt=[]
					Mr_inter_Mt=list(set(rl)&set(l))
					Mr_div_Mt=list(set((rl)).difference(set(Mr_inter_Mt)))

					
					

					S= list(set(CMxCC(q.taf,x,Nx_tomi_Mt)).union(set(Mr_div_Mt)))
					print("S 335", S)
					print("prin to break")
					break
					

			else:	
				print("eimai sto else")
				union_Mt=[]
				
				for child in t:
					print("child root 370",child.root)	
					leaves=[]
					leaves=find_leaves(child,leaves)
					#if (child.root!="1-node" and child.root!="0-node"):
					#	leaves=[]
					
						
					union_Mt = list(set(union_Mt).union(set(leaves)))
				S = union_Mt
				print("S 347", S)
			
			
	else:
		qr=[]
		qxr=[]
		for child in node.children:
			qr.append(child)
			l=[]
			l=find_leaves(child,l)
			#if (child.root!="1-node" and child.root!="0-node"):
			#	l=[]
			print("child", child.root,"leaves",l)
		
			for xi in x_neighbours:
				if xi in l:
					if child not in qxr:
						qxr.append(child)

		print("qxr 400")
		for i in qxr:
			print(i.root)
		print("qr 403")
		for i in qr:
			print(i.root)

			#if qxr and (len(qxr)<len(qr) or len(qxr)==len(qr)):
		#if  len(qxr)==1 and len(qr)==1 and qxr[0]==qr[0]:
		if len(qr)>0 and len(qxr)==1:
			print("qxr root", qxr[0].root)
			print("qr root", qr[0].root)

			S=CMxCC(qxr[0],x,x_neighbours)
		elif len(qxr)==0 and qr:
			print("qr 381", qr)
			print("bika")
			S=CMxCC(qr[0],x,x_neighbours)
			print("S 385", S)
			


		elif len(qxr)>1:

			print("node",node.root)	
			unionMt=[]
			for child in qxr:

				print("test edo" ,child.root)
				cl=[]
				cl=find_leaves(child,cl)
				#if (child.root!="1-node" and child.root!="0-node"):
					#cl=[]
				print("cl", cl)
				unionMt= list(set(unionMt).union(set(cl)))
			print("hey unionMT", unionMt)
			S= unionMt
			print("S 397", S)
	print("S 398", S)
	return S

def add_edges(g, parent, children):

	#while 
	
	for child in children:
		if child.root!="0-node" and child.root!="1-node":
			g.add_edge(parent.root+str(parent.id),child.root)
		else:
			g.add_edge(parent.root+str(parent.id),str(child.root)+str(child.id))


		add_edges(g,child,child.children)


 


	

 
			
def main():
	file_path = 'cograph.json'
	cograph_data = read_graph_from_file(file_path)
	g= make_g(cograph_data)
	#is_cograph(g)
	print("what")
	#b= is_cograph(g)
	#print("B",b)
	if is_cograph(g):
		#print("ITS A COGRAPH")
	
		
		root= createnode(None,0)
		make_cotree(g,root,0)
		print_cotree(root)
		#input , new graph Gx
		length=len(g)
		x=length
		x_neighbours=[] 

		def on_button():
			flag=0
			suc=0
			invalid=0
			v=entry.get()
			y=""
	
			if len(v) ==0:
				
				messagebox.showinfo(message="Please enter a value.")
				flag+=1
			else:
				fl=0
				for i in v:
					if not i.isnumeric():
						fl+=1
				if fl == len(v):
					messagebox.showinfo(message="Invalid input")
					flag+=1
					invalid+=1

			
			if invalid==0:
				for i in v:

					if  i.isnumeric():
		
						y=y+i
						
						if v.index(i)==len(v)-1:
							if int(y) not in range(len(g)):
								flag+=1
								messagebox.showinfo(message="Node "+y+" not found in graph. Nodes must be from 0 to "+str(len(g)-1))
							else:
								x_neighbours.append(int(y))
								suc+=1
								y=""

						
					else:
						

						
						if v.index(i)==len(v)-1:
							

							if int(y) not in range(len(g)):
								flag+=1
								messagebox.showinfo(message="Node "+y+" not found in graph. Nodes must be from 0 to "+str(len(g)-1))
								y=""
							else:
								x_neighbours.append(int(y))
								suc+=1
								y=""
							
							
						else:
							if y=="":
								continue
							
							if int(y) not in range(len(g)):
								flag+=1
								messagebox.showinfo(message="Node "+y+" not found in graph! Nodes must be from 0 to "+str(len(g)-1))
								y=""

							else:
								suc+=1
								x_neighbours.append(int(y))
								y=""
								
			if flag==0 and suc!=0: #if no mistakes destroy window
				window.destroy()

		

		window=tk.Tk()
		window.title("Data Entry Form- Enter new neighbours")
		window.geometry("730x100")
		first_label=tk.Label(text="Please enter the new neighbours of node #"+str(length)+", separated by a comma(,). Enter nodes that range from 0-"+str(len(g)-1)+".")
		first_label.grid(row=0,column=0)
		entry=tk.Entry(window)
		entry.grid(row=5,column=0)
		button=tk.Button(window,text="Click",command= on_button)
		button.grid(row=5,column=1)
		
		
		
		window.mainloop()

		print("X neighbors", x_neighbours)
		
		
	
	
	
	
		Ss= CMxCC(root,x,x_neighbours)
		print("S:  ",Ss)
		Hx=deepcopy(g)
		#for x in x_neighbours:
		#	if x not in Ss:
		#		Ss.append(x)
		
		print("x", x)
		Hx[x]=Ss
		if x_neighbours not in Hx[x]:
			Hx[x]= Hx[x]+x_neighbours
			Hx[x].sort()
		for i in x_neighbours:
			if x not in Hx[i]:
				Hx[i].append(x)
				Hx[i].sort()


		print("Hx", Hx)
		print("x_neighbours", x_neighbours)

		for i in Ss:
			if i in Hx:
				Hx[i].append(x)

		
		if is_cograph(Hx):
			print(Hx)

		G=nx.Graph()
		tree=nx.DiGraph()

		
		#tree.add_node(root.root+"str(0)")
		add_edges(tree, root, root.children)
		


		

			
		
		


		
		for i in Hx:
			

			G.add_node(i)
			for y in Hx[i]:
				if i==x:
					print("hi")
					G.add_edge(i,y,color='r')	
				else:
					G.add_edge(i,y,color='b')
		colors = nx.get_edge_attributes(G,'color').values()
		
		print(G)
		
		plt.figure(1)
		nx.draw_planar(G, with_labels = True, edge_color=colors)

		plt.figure(2)
		 
		nx.draw_circular(tree, with_labels=True)
		#p=nx.drawing.nx_pydot.to_pydot(tree)
		#p.write_png('example.png')
		

		#nx.draw(tree, with_labels=True, node_size=700, node_color='skyblue', font_size=8)



		plt.show()




	

	


	

	
if __name__ == "__main__":
    main()