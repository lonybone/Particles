import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
mouse_radius = 100

gravity = 0.1
num_particles = 20
default_vel = 25
default_size = 10
damping = 0.01
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Particle():
    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2, radius: float, weight: float, damping: float) -> None:
        self.pos = pos
        self.dir = dir
        self.vel = vel
        self.radius = radius
        self.weight = weight
        self.damping = damping

    def update(self, mouse_pos: tuple[int, int], clicked: bool) -> None:

        # Force the particles out of a specific circle
        dist_to_mouse = self.pos.distance_to(mouse_pos)
        if dist_to_mouse <= mouse_radius:
            if clicked:
                self.vel.y += default_vel
            else:
                self.vel += (self.pos - mouse_pos).normalize()

        # Downforce of gravity
        self.vel.y += gravity * self.weight

        # Apply velociy
        self.pos += self.vel

        # Horizontal collisions
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x *= -1

        elif self.pos.x + self.radius >= screen.get_width():
            self.pos.x = screen.get_width() - self.radius
            self.vel.x *= -1

        # Vertical collisions
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y *= -1

        elif self.pos.y + self.radius >= screen.get_height():
            self.pos.y = screen.get_height() - self.radius
            self.vel.y *= -1

        # Apply damping
        self.vel *= (1 - self.damping)

    def draw(self) -> None:
        pygame.draw.circle(screen, BLUE, self.pos, self.radius)

def generate_particles(amount: int) -> list[Particle]:
    ret = []

    for _ in range(amount):
        pos = pygame.Vector2(random.randint(10, screen.get_width() - 10), random.randint(10, screen.get_height() - 10))
        vel = pygame.Vector2.rotate(pygame.Vector2(0, 1), random.random() * math.pi * 2) * (random.random() * default_vel * 2)
        size = random.random() * default_size * 2
        weight = size

        ret.append(Particle(pos, vel, size, weight, damping))

    return ret

def check_collisions(particles: list[Particle]) -> None:
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            dist_vec = p1.pos - p2.pos
            dist_sq = dist_vec.length_squared()
            min_dist_sq = (p1.radius + p2.radius) ** 2

            if dist_sq < min_dist_sq and dist_sq > 0:
                dist = dist_sq**0.5
                normal = dist_vec / dist

                overlap = (p1.radius + p2.radius) - dist
                total_weight = p1.weight + p2.weight

                p1.pos += normal * (overlap * (p2.weight / total_weight))
                p2.pos -= normal * (overlap * (p1.weight / total_weight))

                v1_along_normal = p1.vel.dot(normal)
                v2_along_normal = p2.vel.dot(normal)

                m1, m2 = p1.weight, p2.weight
                new_v1_normal = (v1_along_normal * (m1 - m2) + 2 * m2 * v2_along_normal) / (m1 + m2)
                new_v2_normal = (v2_along_normal * (m2 - m1) + 2 * m1 * v1_along_normal) / (m1 + m2)

                vel_change_1 = (new_v1_normal - v1_along_normal) * normal
                vel_change_2 = (new_v2_normal - v2_along_normal) * normal

                p1.vel += vel_change_1
                p2.vel += vel_change_2


if __name__ == "__main__":

    particles = generate_particles(num_particles)
    clicked = False

    while True:

        clicked = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        screen.fill(BLACK)
        pygame.draw.circle(screen, RED, mouse_pos, mouse_radius, 3)


        for p in particles:
            p.update(mouse_pos, clicked)

        check_collisions(particles)

        for p in particles:
            p.draw()

        pygame.display.flip()
        clock.tick(60)
