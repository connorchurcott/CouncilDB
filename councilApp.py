import sqlite3
conn = sqlite3.connect('council.db')

def Welcome(): 
    print("\nHello, Welcome to the Grant Council Database!")
    print("Please input the number of the option you would like: \n")
    print("(1): Find all competitions with one large proposal ")
    print("(2): Find the proposal that requests the most money ")
    print("(3): Find the proposal that was awarded the largest amount of money ")
    print("(4): Find the discrepancy between a proposals requested and awarded amount ")
    print("(5): Assign a reviewer to a proposal ")
    print("(6): Find the proposals a reviewer needs to complete ")
    print("(7): Exit Program ")
    return input("Enter Number: ")

def optionOne(): 
    month = input("Please enter the start month (01-12) of the competitions you would like to search: ")
    query = "SELECT C.competitionID, C.title FROM Competitions C JOIN Proposals P ON P.competitionID = C.competitionID WHERE C.applicationDate LIKE '%%%%-' || :month || '-%%' AND P.amountReq > 20000"

    cur = conn.cursor()
    cur.execute(query,{"month":month})
    rows = cur.fetchall()

    if rows: 
        print("\nHere is the competitions with large proposals starting in", month)
        for row in rows:
            print("competitionID: ", row[0])
            print("title: ", row[1])
            print("\n")
    else: 
        print("\nThere are no competitions with large proposals in", month )

    cur.close()

def optionTwo(): 
    compID = input("Please enter the competitionID (300-309) to find the highest requested amount by a propasl in that competition: ")
    query = "SELECT P.proposalID FROM Proposals P WHERE P.competitionID = :compID AND P.amountReq = (SELECT MAX(amountReq) FROM Proposals WHERE competitionID = :compID)"

    cur = conn.cursor()
    cur.execute(query,{"compID":compID})
    rows = cur.fetchall()

    if rows: 
        print("\nHere is the proposal with the highest amountReq for the competion", compID)
        for row in rows:
            print("proposalID: ", row[0])
            print("\n")
    else: 
        print("\nThere are no proposals for the competition", compID)

    cur.close()
    
def optionThree(): 
    date = input("Please enter the date (YYYY-MM-DD) you would like to search before to find the maximum awarded proposal: ")
    query = "SELECT P.proposalID FROM Proposals P WHERE P.date < :date AND P.amountReq = (SELECT MAX(amountReq) FROM Proposals WHERE date < :date)"

    cur = conn.cursor()
    cur.execute(query,{"date":date})
    rows = cur.fetchall()

    if rows: 
        print("\nHere is the proposal with the highest amountReq before", date)
        for row in rows:
            print("proposalID: ", row[0])
            print("\n")
    else: 
        print("\nThere are no proposals before", date)

    cur.close()

def optionFour(): 
    compID = input("Please input the competitionID (300-309) that you would like to find the average discrepenacy of: ")
    query = "SELECT AVG(ABS(P.amountReq - P.awarded)) FROM Proposals P JOIN Competitions C ON C.competitionID = P.competitionID WHERE C.competitionID = :compID"

    cur = conn.cursor()
    cur.execute(query,{"compID":compID})
    rows = cur.fetchall()

    if rows: 
        print("\nHere is the average descrepancy from compeition", compID)
        for row in rows:
            print("Average Descrepacncy: ", row[0])
            print("\n")
    else: 
        print("\nThere are no proposals for", compID)

    cur.close()

def optionFive(): 
    propID = input("Please input the proposalID (200-214) of the proposal you would like to assign: ")
    queryConflicts = "SELECT DISTINCT R.reviewerID FROM Reviewers R WHERE R.reviewerID NOT IN (SELECT DISTINCT C.reviewerID1 FROM CONFLICTS C WHERE C.reviewerID2 = (SELECT P.researcherID FROM Proposals P WHERE P.proposalID = :propID) UNION SELECT DISTINCT C.reviewerID2 FROM Conflicts C WHERE C.reviewerID1 = (SELECT P.researcherID FROM Proposals P WHERE P.proposalID = :propID))"
    
    cur = conn.cursor()
    cur.execute(queryConflicts,{"propID":propID})
    rows = cur.fetchall()

    if rows: 
        print("\nHere is the list of reivewers that are allowed to review", propID)
        for row in rows:
            print("reviewerID: ", row[0])
            print("\n")
    else: 
        print("\nThere are no eligable reivewers for", propID)

    cur.execute("SELECT MAX(RPID) FROM ReviewedProposals")
    nextRPID = cur.fetchone()[0] + 1

    compQuery = "SELECT DISTINCT C.competitionID FROM Competitions C JOIN Proposals P ON P.competitionID = C.competitionID WHERE P.proposalID = :propID"
    cur.execute(compQuery, {"propID":propID})
    compID = cur.fetchone()[0]


    revID  = input("Please input the reviewerID of whom you would like to assign: ")
    date = input("Please input the due date for this assignment (YYYY-MM-DD): ")

    insert = "INSERT INTO ReviewedProposals (RPID, proposalID, reviewerID, competitionID, deadline, status) VALUES (?, ?, ?, ?, ?, ?)"
    values = (nextRPID, propID, revID, compID, date, "not submitted")
    cur.execute(insert, values)

    conn.commit()
    cur.close()

def optionSix(): 
    name = input("Please enter the first name of the reviewer who you would like to search: ")
    query = "SELECT Rp.proposalID FROM ReviewedProposals Rp JOIN Reviewers Re ON Re.reviewerID = Rp.reviewerID JOIN Researchers R ON R.researcherID = Re.reviewerID WHERE R.firstName = :name"

    cur = conn.cursor()
    cur.execute(query,{"name":name})
    rows = cur.fetchall()

    if rows: 
        print("\nHere are all the incompleted reviews by", name)
        for row in rows:
            print("proposalID: ", row[0])
            print("\n")
    else: 
        print("\nThere are no reviewers by this name with pending reviews")

    cur.close()

def optionSelect(option): 
    if option == '1': 
        optionOne()
    elif option == '2': 
        optionTwo()
    elif option == '3': 
        optionThree()
    elif option == '4': 
        optionFour()
    elif option == '5': 
        optionFive()
    elif option == '6': 
        optionSix()


option = Welcome()

while option != '7': 
    optionSelect(option)
    option = Welcome()

print("\nGoodbye.")
conn.close()