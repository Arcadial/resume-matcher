import textdistance as td


def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = (j + s + c + o) / 4
    # total = (s+o)/2
    return total * 100


def keyword_match(resume, job_description):
    """Matches keywords from resume with keywords from job_description.

    Parameters (2)
    resume : pandas dataframe
    job_description : pandas dataframe
    ----------
    Returns
    -------
    job_output_ordered : pandas dataframe
    """
    # Cleaning
    # resume = resume.drop(columns="Unnamed: 0")
    resume["tf_based"][0]

    # List of dictionaries
    # job_description

    # List to store all the keyword similarity scores
    jobs_scoring = []
    # Perform comparison against each job description against Resume
    for job_index in range(len(job_description)):
        temp_score = match(
            resume["tf_based"][0], job_description["tf_based"][job_index]
        )
        jobs_scoring.append(temp_score)
    # Save these scores back to job_output dataframe
    job_description["scores"] = jobs_scoring
    # Order the jobs based on similarity scoring
    job_output_ordered = job_description.sort_values(
        by=["scores"], ascending=False
    ).reset_index(drop=True)

    return job_output_ordered
