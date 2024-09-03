from tanks import EnemyTank
import copy
import pygame



class Cell:
    """класс ячейки  матрицы """

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) # её объект rect для удобной проверки на пересечения
        self.free = True # ячейка занята препятсвием или нет
    
    def __str__(self):
        """функция для удобного прочтчения матрицы"""
        ans = str(self.free)
        return ans + " " * (5 - len(ans))


class AStar:
    """класс описывающий алгоритм astar - bfs на матртице"""

    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self, W, H, size):
        self.dW = 25 # size[0] 
        self.dH = 25 # size[0] 
        self.W = (W - 25) // self.dW  # ширина матрицы
        self.H = (H - 25) // self.dH # высота матрицы
        self.matrix = [[Cell(x * self.dW + 20, y * self.dH + 20, self.dW, self.dH) for y in range(self.H)] for x in range(self.W)]
        # 20 это свиг щасчёт граничных препятсвий


    def save_obstacles(self, obstacles):
        """запсиывает в матрице какие клетки закрыты для проезда засчёт препятствий"""
        self.obstacles = obstacles
        for i in obstacles:
             for x in range(len(self.matrix)):
                 for y in range(len(self.matrix[x])):
                     if i.rect.colliderect(self.matrix[x][y].rect):
                         self.matrix[x][y].free = False
    

    def bfs(self, tank, enemy_tank):
        """алгоритм bfs на матрицы"""
        visited = [[-1 for _ in range(self.H)] for _ in range(self.W)] 
        # -1 это ячейка не посещена всё остальное показывает растояние до неё
        tank_cor, enemy_tank_cor = tank.center(), enemy_tank.center()
        start_x = (tank_cor[0] - 20) // self.dW
        start_y = (tank_cor[1] - 20) // self.dH
        queue  = [(start_x, start_y)]
        color = 0
        visited[start_x][start_y] = color
        color += 1
        flag = True
        index_queue = 0 # индекс первой не обработаной вершины в очереди
        while flag:
            flag = False
            timed_index_queue = len(queue)

            for i in range(index_queue, len(queue)):
                x, y = queue[i]
                if enemy_tank_cor == (x, y):
                    flag = False
                    break
                for dx, dy in self.moves:
                    x1, y1 = x + dx, y + dy
                    if x1 < 0 or x1 >= self.W or y1 < 0 or y1 >= self.H:
                        continue
                    if visited[x1][y1] == -1 and self.matrix[x1][y1].free:
                        queue.append((x1, y1))
                        flag = True
                        visited[x1][y1] = color
            index_queue = timed_index_queue
            color += 1
        x, y = (enemy_tank_cor[0] - 20) // self.dW, (enemy_tank_cor[1] - 20) // self.dH
        if visited[x][y] == -1:
            return 
        # выбор наиболее оптимального направления ans = 0
        x_ans, y_ans = x, y
        for i in range(len(self.moves)):
            dx, dy = self.moves[i]
            x_timed, y_timed = x + dx, y + dy   
            if x_timed < 0 or x_timed >= self.W or y_timed < 0 or y_timed >= self.H:
                continue
            if visited[x_timed][y_timed]  == visited[x][y] - 1 and visited[x_timed][y_timed] != -1 and self.matrix[x_timed][y_timed]:
                x_ans, y_ans = x_timed, y_timed
                ans = i

        return ["up", "down", "left", "right"][ans]

        
