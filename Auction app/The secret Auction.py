from linecache import clearcache

bids={
}
maxim=0
should_continue="y"
while should_continue=="y":
	name = input("What is your name ?\n")
	value = int(input("What is your bid ?\n $"))
	bids[name]=value
	should_continue = input("It s another person there that want to bid  ? [y/n]")
	print("\n"*1000)
maxim = max(bids.values())
for name, bid in bids.items():
	if bid == maxim:
		print(f"Persoana care a licitat cel mai mult este {name} cu suma de {bid}")


