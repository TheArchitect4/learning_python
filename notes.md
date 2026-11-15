# learning_python
Random stuff





*** Pervious colision code

only bounce if they are moving away from eachother, idk these impilse mechanmcis tho, i used a vector projection method but it wasnt working
city_along_norm < 0:
    body1["velocity_x"] -= (2 * body2["mass"]) / (body1["mass"] + body2["mass"]) * velocity_along_norm * norm_x * bounciness
    body1["velocity_y"] -= (2 * body2["mass"]) / (body1["mass"] + body2["mass"]) * velocity_along_norm * norm_y * bounciness

    body2["velocity_x"] += (2 * body1["mass"]) / (body1["mass"] + body2["mass"]) * velocity_along_norm * norm_x * bounciness
    body2["velocity_y"] += (2 * body1["mass"]) / (body1["mass"] + body2["mass"]) * velocity_along_norm * norm_y * bounciness

    basically we have this mass factor multiplied by the velocity along the normal and break that up into components and multiply that by bounciness so that its not perfectly elastic. 

    i think the problem was with how i defined my norm and then how i wsas adding these calculations becasue sometimes itd add speed
