import textdistance as td


def match(resume, job_des):
    c = td.cosine.similarity(resume, job_des)
    #total = (s+o)/2
    return c*100
