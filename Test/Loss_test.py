import torch


x=torch.ones(1,51)
#x[0].fill_(2)



#x=x.clamp(2,4)


print (x)
#print(x.uniform_(-1,1))

#x.fill_(2)
#print(x)

#print(x[0])
#print(torch.norm(x[0]))
# somma il quadrato dei componenti della matrice e poi esegue la radice quadrata con p=2
# p = potenza utilizzata
# somma il cubo dei componenti della matrice e poi esegue la radice cubica con p=3
#dim=0 seleziona le colonne
#dim=1 seleziona le righe
norm=torch.norm(x,p=2,dim=0)

output= torch.div(x,norm)

print(norm)
print(output)


