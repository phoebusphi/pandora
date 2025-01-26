import os
import numpy as np
import random as rd
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def offspring(parents:np.ndarray)->np.ndarray:
    babys = np.zeros(parents.shape)
    split = np.random.randint(0,parents.shape[1])
    babys[0,:split] = parents[0,:split]
    babys[0,split:] = parents[1,split:]
    babys[1,:split] = parents[1,:split]
    babys[1,split:] = parents[0,split:]
    return babys

class GAtelco:


    num_routers = 1

    def __init__(self, mu=0.75, eta=0.22,
                        generations:int=3000,
                        people_priority:dict={"tipo1":50,"tipo2":200,"tipo3":800},
                        pop_size:int=100):
        self.generations=generations
        self.mu = mu
        self.eta = eta
        self.pop_size = pop_size
        self.num_user_p1 = people_priority["tipo1"]
        self.num_user_p2 = people_priority["tipo2"]
        self.num_user_p3 = people_priority["tipo3"]

    def init_people(self):
        usuario = { "tipo1":np.array([np.random.normal(150,20,2) for _ in range(self.num_user_p1)]),
                    "tipo2":np.array([np.random.normal(170,30,2) for _ in range(self.num_user_p2)]),
                    "tipo3":np.array([np.random.normal(170,30,2) for _ in range(self.num_user_p3)])}
        return usuario

    def population(self):
        return np.random.randint(100,1000,(self.pop_size,2)) if self.num_routers==1 else np.random.randint(100,1000,(self.pop_size,2, self.num_routers))

    def selection(self, pop_tmp:np.ndarray, l_eval:list)->dict:
        rows, cols = pop_tmp.shape
        winners = np.zeros(rows//2,dtype=int)
        eval_pop = np.array(l_eval)
        father = np.zeros((rows//2,cols))
        list_pop = np.arange(0,100).reshape(50,2)
        np.random.shuffle(list_pop)
        i = 0
        while i<50:
            row = list_pop[i, :]
            index = np.where(eval_pop[row]==np.max(eval_pop[row]))[0][0]
            father[i,:] = pop_tmp[row[index], :]
            np.put(winners, i, row[index])
            i+=1
        list_pop = list_pop.flatten()
        list_pop = np.delete(np.sort(list_pop),winners, None)
        mother = pop_tmp[list_pop,:]
        return {'father':father, 'mother':mother}

    def cross(self, pop_gen:np.ndarray, best:np.ndarray, eval_pop)->np.ndarray:
        pop_tmp = pop_gen.copy()
        new_pop = np.zeros(pop_gen.shape)
        men_woman = self.selection(pop_tmp=pop_tmp, l_eval=eval_pop)
        father, mother = men_woman['father'], men_woman['mother']
        r_u, r_d = 0, 2
        for f, m in zip(father, mother):
            parents = np.matrix([f,m])
            if rd.random() < self.mu:
                new_pop[r_u:r_d,:]= offspring(parents=parents)
            else:
                new_pop[r_u:r_d,:] = parents
            r_u = r_d
            r_d += 2
        new_pop[0, :] = best
        return new_pop

    def mutation(self, pop_tmp):
        eta_mat = np.random.random(self.pop_size)
        mut_eta = np.where(eta_mat<=self.eta)[0]
        count_mod = mut_eta.size
        pop_tmp[mut_eta, :] = np.random.randint(100,500,(count_mod, 2))
        return pop_tmp


    def fx(self, pop_tmp:np.ndarray)->tuple:
        c = 2/(10^6)
        L_total = np.zeros((self.pop_size))
        L_tipo1 = np.zeros((self.pop_size))
        k=0
        distribution_people = self.init_people()
        ponderacion = [80,10,10]
        for row in pop_tmp:
            i=0
            L = np.zeros((3))
            for prioridad in distribution_people:
                lim_sup, penality = 0, 0
                if prioridad=="tipo1":
                    lim_sup=15 #ms
                    penality = 100
                elif prioridad=="tipo2":
                    lim_sup=50
                    penality = 30
                else:
                    lim_sup=100
                    penality = 10
                d = np.sqrt(np.sum(np.power(row-distribution_people[prioridad],2),axis=1))
                l_tmp = c*d
                l_tmp = np.where(l_tmp>lim_sup, l_tmp+penality, l_tmp)
                L[i] = ponderacion[i]*np.sum(l_tmp)/100 if i!=0 else ponderacion[i]*np.max(l_tmp)/100
                i+=1
            L_total[k] = np.mean(L)
            L_tipo1[k] = L[0]
            k+=1
            del L
        return  L_total, L_tipo1

    def get_fitness(self,pop_gen:np.ndarray)->tuple:
        eval, eval_tipo1 = self.fx(pop_tmp= pop_gen)
        fitness_tipo1_index = np.argmin(eval_tipo1).item()
        fitness_index = np.argmin(eval).item()
        best_ind = pop_gen[fitness_index]
        fitness = eval[fitness_index]
        fitness_tipo1 = eval_tipo1[fitness_tipo1_index]
        return (eval, best_ind, fitness, fitness_tipo1)

    def GA(self)->dict:
        df_result = {'generacion':np.arange(self.generations),'optimal':[],'avg':[]}
        dominio = []; imagen = []; pop_avg = []
        imagen = np.zeros(self.generations); pop_avg = np.zeros(self.generations)
        dominio = np.zeros((self.generations, 2)); imagen_tipo1 = np.zeros(self.generations)
        pop = self.population()
        eval, best_ind, fitness, fit_tipo1 = self.get_fitness(pop_gen=pop)
        dominio[0, :] = best_ind
        imagen[0] = fitness
        imagen_tipo1[0] = fit_tipo1
        pop_avg[0] = np.mean(eval)
        for generation in range(1,self.generations):
            pop_tmp = self.cross(pop_gen=pop, best=best_ind, eval_pop=eval)
            pop_tmp = self.mutation(pop_tmp=pop_tmp)
            pop = pop_tmp.copy()
            eval, best_ind, fitness, fit_tipo1 = self.get_fitness(pop_gen=pop)
            pop_avg[generation] = np.mean(eval)
            if fitness < imagen[generation-1]:
                imagen[generation] = fitness
                imagen_tipo1[generation] = fit_tipo1
                dominio[generation, :] = best_ind
            else:
                imagen[generation] = imagen[generation-1]
                imagen_tipo1[generation] = imagen_tipo1[generation-1]
                dominio[generation, :] = dominio[generation-1]
            print("generacion {0} | fitness_optimo {1} | fitness_tipo1 {2}".format(generation,imagen[generation], imagen_tipo1[generation]))
        df_result['optimal'] = imagen
        df_result['optimal_tipo1'] = imagen_tipo1
        #df_result["position_optimal"] = list(dominio)
        df_result['avg'] = pop_avg
        df_result = pd.DataFrame(df_result)
        self.plot_optimal(df_result, dominio)
        df_result.to_csv("./resultado_"+str(self.generations)+".csv")
        return {'dominio':dominio, 'imagen':imagen}

    def plot_optimal(self,df_result, dominio):
        fig, ax = plt.subplots(nrows=1, ncols=2)
        ax[0].plot(df_result.optimal.values)
        ax[1].plot(df_result.optimal_tipo1.values)
        ax[0].set_title("Best individuo")
        ax[0].set_xlabel("generation")
        ax[0].set_ylabel("Latency (ms)")
        ax[1].set_title("Best latency on Priority 1")
        ax[1].set_xlabel("generation")
        ax[1].set_ylabel("Latency (ms)")
        fig.tight_layout()
        plt.savefig("optimal.jpg")
        users=self.init_people()
        for i in range(self.generations):
            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.plot(dominio[i][0],dominio[i][1], "*", c="red", label="Router", markersize= 30)
            ax.plot(users["tipo1"][:,0],users["tipo1"][:,1], ".", label="Priority 1", c="lime")
            ax.plot(users["tipo2"][:,0],users["tipo2"][:,1], ".", label="Priority 2", c="purple")
            ax.plot(users["tipo3"][:,0],users["tipo3"][:,1], ".", label="Priority 3", c="black")
            plt.xlabel("Longitude")
            plt.xlabel("Latitude")
            plt.title("Optimal Distribution of a Router")
            plt.savefig("./images_gif/generation_{}.jpg".format(i))







def create_gif(image_folder, gif_filename, duration=100):
    """
    Convierte imágenes JPG de una carpeta en un GIF animado.

    Parámetros:
    - image_folder: Ruta de la carpeta con las imágenes
    - gif_filename: Nombre del archivo GIF de salida
    - duration: Tiempo de visualización de cada imagen en milisegundos (por defecto 500)
    """
    # Obtener lista de archivos de imagen, ordenados alfabéticamente
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    images.sort()  # Ordenar para asegurar secuencia consistente

    # Lista para almacenar los frames
    frames = []

    # Abrir y procesar cada imagen
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        img = Image.open(image_path)

        # Convertir a modo RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')

        frames.append(img)

    # Guardar el GIF
    frames[0].save(
        gif_filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0  # 0 significa bucle infinito
    )

    print(f"GIF creado exitosamente: {gif_filename}")

# Ejemplo de uso

# Reemplaza 'ruta/a/tu/carpeta/de/imagenes' con la ruta real de tus imágenes
#GAtelco(mu=0.75, eta=0.22, generations=2000).GA()
#create_gif('./images_gif/', 'output.gif')
