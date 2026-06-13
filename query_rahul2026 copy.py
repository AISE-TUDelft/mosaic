from typing import Optional

# Collect initial information about each PR
# Should scrape from January 1st 2023 until current date.
# after parameter was initially used for pagination, but no longer needed if you handle pagination internally
# Similarly, you can remove the filter parameter within the search, it was initially used to get PRs for a certain agent. Now we want to collect ALL PRs, irrespective of the authorship. We'll perform the filtering afterwards.
    
    


# Get review information from each PR, based on the PR IDs already collected.
def pr_review_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        reviewRequests(first: 100) {{
                            totalCount
                            nodes {{
                                id
                                databaseId
                                asCodeOwner
                                requestedReviewer {{
                                    __typename
                                    ... on User {{
                                        id
                                        databaseId
                                        login
                                        avatarUrl
                                        url
                                    }}
                                    ... on Bot {{
                                        id
                                        databaseId
                                        login
                                        avatarUrl
                                        url
                                    }}
                                    ... on Team {{
                                        id
                                        databaseId
                                        name
                                        slug
                                        url
                                    }}
                                }}
                            }}
                        }}
                        reviewThreads(first: 100) {{
                            totalCount
                            nodes {{
                                id
                                isCollapsed
                                diffSide
                                isOutdated
                                isResolved
                                line
                                originalLine
                                originalStartLine
                                path
                                startDiffSide
                                startLine
                                comments {{
                                    totalCount
                                }}
                                resolvedBy {{
                                        login
                                        avatarUrl
                                        url
                                        __typename
                                    }}
                                subjectType 
                            }}  
                        }}
                        reviews(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    fullDatabaseId
                                    authorAssociation
                                    author {{
                                        login
                                        avatarUrl
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                    body
                                    bodyText
                                    createdAt
                                    editor {{
                                        avatarUrl
                                        login
                                        resourcePath
                                        url
                                        __typename 
                                    }}
                                    includesCreatedEdit
                                    isMinimized
                                    lastEditedAt
                                    minimizedReason
                                    publishedAt
                                    resourcePath
                                    reactionGroups {{
                                        createdAt
                                        content
                                        subject {{
                                            databaseId
                                            id  
                                        }}
                                        reactors(first: 100) {{
                                            totalCount
                                            nodes {{
                                                __typename  
                                            }}
                                        }}
                                    }}
                                    reactions(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            databaseId
                                            content
                                            createdAt
                                            user {{
                                                id
                                                databaseId
                                                createdAt
                                                login
                                                url
                                                __typename
                                        }}
                                    }}
                                }}
                                comments(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        fullDatabaseId
                                        body
                                        bodyText
                                        createdAt
                                        diffHunk
                                        line
                                        lastEditedAt
                                        outdated
                                        originalLine
                                        originalStartLine
                                        path
                                        publishedAt
                                        state
                                        startLine
                                        subjectType
                                        url
                                        updatedAt
                                    }}
                                }}
                                state
                                repository {{
                                    id
                                    databaseId
                                    name
                                    url
                                    sshUrl
                                    createdAt
                                    description
                                    isPrivate
                                    forkCount
                                    stargazerCount
                                    labels {{
                                        totalCount
                                    }}
                                    languages {{
                                        totalCount
                                    }}
                                    primaryLanguage {{
                                        id
                                        color
                                        name
                                    }}
                                }}
                                submittedAt
                                updatedAt
                                url
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query
    

    
    
# Get commit information from each PR, based on the PR IDs already collected.   
def pr_commit_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        mergeCommit {{
                            id
                            oid
                            url
                            message
                            messageBody
                            messageHeadline
                            abbreviatedOid
                            additions
                            associatedPullRequests(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    fullDatabaseId
                                    title
                                    url
                                    number
                                    state
                                    locked
                                    closed
                                    mergeable
                                    merged
                                    body
                                    bodyText
                                    createdAt
                                    mergedAt
                                    closedAt
                                    updatedAt
                                    lastEditedAt
                                    publishedAt
                                    reviewDecision
                                    isDraft
                                    isReadByViewer
                                    isMergeQueueEnabled
                                    isInMergeQueue
                                    mergeStateStatus
                                    isCrossRepository
                                    canBeRebased
                                    changedFiles
                                    additions
                                    deletions
                                    headRefName
                                    headRefOid
                                    baseRefName
                                    baseRefOid                                                       
                                }}
                            }}
                            authoredDate
                            authoredByCommitter
                            changedFilesIfAvailable
                            commitUrl
                            committedDate
                            deletions
                            author {{
                                name
                                email
                                date
                                user {{
                                    id
                                    databaseId
                                    login
                                    avatarUrl
                                    url
                                    __typename
                                }}
                            }}
                            committer {{
                                name
                                email
                                date
                                user {{
                                    id
                                    databaseId
                                    login
                                    avatarUrl
                                    url
                                    __typename
                                }}
                            }}
                        }}
                        commits(first: 100) {{
                            totalCount
                            nodes {{
                                id
                                resourcePath
                                url
                                commit {{
                                    abbreviatedOid
                                    id
                                    oid
                                    url
                                    message
                                    messageBody
                                    messageHeadline
                                    abbreviatedOid
                                    additions
                                    associatedPullRequests(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            fullDatabaseId
                                        }}
                                    }}
                                    author {{
                                        email
                                        name
                                        date
                                        user {{
                                            id
                                            databaseId
                                            login
                                            avatarUrl
                                            url
                                            __typename
                                        }}
                                    }}
                                    authoredByCommitter
                                    authoredDate
                                    changedFilesIfAvailable
                                    authors(first: 100) {{
                                        totalCount
                                        nodes {{
                                            email
                                            name
                                            date
                                            user {{
                                                id
                                                databaseId
                                                login
                                                avatarUrl
                                                url
                                                __typename
                                            }}
                                        }} 
                                    }}
                                    commitResourcePath
                                    commitUrl
                                    committedDate
                                    committer {{
                                        email
                                        name
                                        date
                                        user {{
                                            id
                                            databaseId
                                            login
                                            avatarUrl
                                            url
                                            __typename
                                        }}
                                    }}
                                    deletions
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query          
    
    
    
    
    

# Get comment information from each PR, based on the PR IDs already collected.
def pr_comment_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        comments(first: 100) {{
                            totalCount
                            nodes {{
                                id
                                databaseId
                                author {{
                                    __typename
                                    login
                                    url
                                    avatarUrl
                                    ... on User {{
                                        id
                                        databaseId
                                    }}
                                }}
                                authorAssociation
                                body
                                bodyText
                                createdAt
                                includesCreatedEdit
                                isMinimized
                                lastEditedAt
                                issue {{
                                    id
                                    databaseId
                                    title
                                    url
                                    body
                                    bodyText
                                    number
                                    createdAt
                                    closed
                                    closedAt
                                    labels {{
                                        totalCount
                                    }}
                                }}
                                minimizedReason
                                publishedAt
                                reactions(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        content
                                        createdAt
                                        user {{
                                            id
                                            databaseId
                                            login
                                            url
                                            __typename
                                        }}
                                    }}
                                }}
                                updatedAt
                                url
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query    



# Get issue information from each PR, based on the PR IDs already collected.
def pr_closing_issue_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        closingIssuesReferences(first: 100) {{
                            totalCount
                            nodes {{
                                id
                                databaseId
                                createdAt
                                title
                                url
                                body
                                bodyText
                                bodyResourcePath
                                bodyUrl
                                number
                                activeLockReason
                                assignedActors(first: 100) {{
                                    totalCount
                                    nodes {{
                                        __typename
                                        ... on User {{
                                            id
                                            databaseId
                                            login
                                            name
                                            avatarUrl
                                            url
                                        }}
                                        ... on Bot {{
                                            id
                                            databaseId
                                            login
                                            avatarUrl
                                            url
                                        }}
                                        ... on Organization {{
                                            id
                                            databaseId
                                            login
                                            name
                                            avatarUrl
                                            url
                                        }}
                                        ... on Mannequin {{
                                            id
                                            databaseId
                                            login
                                            name
                                            avatarUrl
                                            url
                                        }}
                                    }}
                                }}
                                author {{
                                    avatarUrl
                                    login
                                    __typename
                                    ... on User {{
                                            id
                                            databaseId
                                            bio
                                            avatarUrl
                                            createdAt
                                            email
                                            url
                                            websiteUrl
                                            userViewType
                                            estimatedNextSponsorsPayoutInCents
                                            commitComments {{
                                                totalCount
                                            }}
                                            company
                                            contributionsCollection {{
                                                commitContributionsByRepository {{
                                                    url
                                                    resourcePath
                                                    contributions {{
                                                        totalCount
                                                    }}
                                                    repository {{
                                                        id
                                                        databaseId
                                                        name
                                                        url
                                                        sshUrl
                                                        createdAt
                                                        description
                                                        isPrivate
                                                        forkCount
                                                        stargazerCount
                                                        labels {{
                                                            totalCount
                                                        }}
                                                        languages {{
                                                            totalCount
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                }}
                                            contributionCalendar {{
                                                colors
                                                isHalloween
                                                totalContributions
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
                                                    __typename
                                                }}
                                            }}
                                            firstPullRequestContribution {{
                                                ... on CreatedPullRequestContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
                                                    __typename 
                                                }}
                                            }}
                                            firstRepositoryContribution {{
                                                ... on CreatedRepositoryContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url 
                                                    __typename
                                                }}
                                            }}
                                            hasActivityInThePast
                                            hasAnyContributions
                                            hasAnyRestrictedContributions
                                            isSingleDay
                                            issueContributions {{
                                                totalCount
                                            }}
                                            issueContributionsByRepository {{
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions {{
                                                totalCount
                                            }}
                                            pullRequestContributionsByRepository {{
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions {{
                                                    totalCount
                                                }}      
                                            }}
                                            pullRequestReviewContributions {{
                                                totalCount
                                            }}
                                            repositoryContributions {{
                                                totalCount
                                            }}
                                            startedAt
                                            totalCommitContributions
                                            totalIssueContributions
                                            totalPullRequestContributions
                                            totalPullRequestReviewContributions
                                            totalRepositoriesWithContributedCommits
                                            totalRepositoriesWithContributedIssues
                                            totalRepositoriesWithContributedPullRequestReviews
                                            totalRepositoriesWithContributedPullRequests
                                            totalRepositoryContributions
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(first: 100) {{
                                            totalCount
                                        }}
                                        gists {{
                                            totalCount
                                        }}
                                        hasSponsorsListing
                                        isBountyHunter
                                        isCampusExpert
                                        isDeveloperProgramMember
                                        isEmployee
                                        isGitHubStar
                                        isHireable
                                        isSiteAdmin
                                        issueComments {{
                                            totalCount
                                        }}
                                        issues{{
                                            totalCount
                                        }}
                                        lifetimeReceivedSponsorshipValues {{
                                            totalCount
                                        }}
                                        lists {{
                                            totalCount
                                        }}
                                        location
                                        login
                                        monthlyEstimatedSponsorsIncomeInCents
                                        name
                                        organizations{{
                                            totalCount
                                        }}
                                        packages {{
                                            totalCount
                                        }}
                                        projectsResourcePath
                                        projectsUrl
                                        pronouns
                                        pullRequests {{
                                            totalCount
                                        }}
                                        repositories {{
                                            totalCount
                                        }}
                                        repositoriesContributedTo {{
                                            totalCount
                                        }}
                                        repositoryDiscussionComments {{
                                            totalCount
                                        }}
                                        repositoryDiscussions{{
                                            totalCount
                                        }}
                                        socialAccounts {{
                                            totalCount
                                        }}
                                        sponsoring {{
                                            totalCount
                                        }}
                                        sponsors {{
                                            totalCount
                                        }}
                                        starredRepositories {{
                                            totalCount
                                            isOverLimit
                                        }}
                                        status {{
                                            id
                                            createdAt
                                            emoji
                                            expiresAt
                                            indicatesLimitedAvailability
                                            message
                                            updatedAt
                                        }}
                                        topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt  
                                        __typename
                                    }} 
                                }}
                                authorAssociation
                                blockedBy(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        createdAt
                                        title
                                        url
                                        body
                                        bodyText
                                         labels {{
                                             totalCount
                                         }}
                                        closed
                                        closedAt
                                    }}
                                }}
                                blocking(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        createdAt
                                        title
                                        url
                                        body
                                        bodyText
                                         labels {{
                                             totalCount
                                         }}
                                        closed
                                        closedAt
                                    }}
                                }}
                                labels {{
                                    totalCount
                                }}
                                closed
                                closedAt
                                closedByPullRequestsReferences(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        fullDatabaseId
                                        title
                                        url
                                        number
                                        state
                                        locked
                                        closed
                                        mergeable
                                        merged
                                        body
                                        bodyText
                                        createdAt
                                        mergedAt
                                        closedAt
                                        updatedAt
                                        lastEditedAt
                                        publishedAt
                                        reviewDecision
                                        isDraft
                                        isReadByViewer
                                        isMergeQueueEnabled
                                        isInMergeQueue
                                        mergeStateStatus
                                        isCrossRepository
                                        canBeRebased
                                        changedFiles
                                        additions
                                        deletions
                                        activeLockReason
                                        createdViaEmail
                                        includesCreatedEdit
                                        maintainerCanModify
                                        checksUrl
                                        revertUrl
                                        permalink 
                                        resourcePath
                                        revertResourcePath 
                                        authorAssociation
                                        totalCommentsCount
                                        baseRefName
                                        baseRefOid
                                        headRefName
                                        headRefOid
                                    }}
                                }}
                                comments(first: 100) {{
                                    totalCount
                                }}
                                duplicateOf {{
                                    id
                                    databaseId
                                    createdAt
                                    title
                                    url
                                    body
                                    bodyText
                                    bodyResourcePath
                                    bodyUrl
                                }}
                                editor {{
                                    avatarUrl
                                    login
                                    __typename 
                                }}
                                includesCreatedEdit
                                lastEditedAt
                                issueDependenciesSummary {{
                                    totalBlockedBy
                                    totalBlocking
                                    blocking
                                    blockedBy
                                }}
                                issueFieldValues(first: 100) {{
                                    totalCount
                                    nodes {{
                                        __typename
                                    }}
                                }}
                                issueType {{
                                    id
                                    color
                                    description
                                    isEnabled
                                    name
                                }}
                                locked
                                linkedBranches(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        ref {{
                                            id
                                            name
                                            prefix
                                        }}
                                    }}
                                }}
                                milestone {{
                                    id
                                    closed
                                    closedAt
                                    closedIssueCount
                                    createdAt
                                    description
                                    dueOn
                                    number
                                    openIssueCount
                                    state
                                    resourcePath
                                    title
                                    updatedAt
                                    url
                                }}
                                parent {{
                                    id
                                    databaseId
                                    title
                                    url
                                    body
                                    bodyText
                                    labels {{
                                        totalCount
                                    }}
                                    createdAt
                                    closed
                                    closedAt 
                                }}
                                participants(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        avatarUrl
                                        createdAt
                                        login
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                }}
                                publishedAt
                                reactions(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        content
                                        createdAt
                                        user {{
                                            id
                                            databaseId
                                            login
                                            url
                                            __typename
                                        }}
                                    }}
                                }}
                                resourcePath
                                state
                                stateReason
                                subIssues(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        title
                                        url
                                        body
                                        bodyText
                                        number
                                        createdAt
                                        closed
                                        closedAt
                                        labels {{
                                            totalCount
                                        }}
                                    }}
                                }}
                                subIssuesSummary {{
                                    completed
                                    percentCompleted
                                    total
                                }}
                                timelineItems(first: 100) {{
                                    totalCount
                                    filteredCount
                                    updatedAt
                                    nodes {{                                         __typename                                     }}
                                }}
                                trackedInIssues(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        title
                                        url
                                        body
                                        bodyText
                                        number
                                        createdAt
                                        closed
                                        closedAt
                                        labels {{
                                            totalCount
                                        }}
                                    }}
                                }}
                                trackedIssues(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        title
                                        url
                                        body
                                        bodyText
                                        number
                                        createdAt
                                        closed
                                        closedAt
                                        labels {{
                                            totalCount
                                        }}
                                    }}
                                }}
                                trackedIssuesCount
                                updatedAt
                                userContentEdits(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        createdAt
                                        deletedAt
                                        deletedBy {{
                                            avatarUrl
                                            login
                                            url
                                            __typename
                                        }}
                                        updatedAt
                                        diff
                                    }}
                                }}
                                locked
                            }}                                        
                        }}
                    }}
                }}
            }}
        """
    return query


# Get repo information from each PR, based on the PR IDs already collected.
def pr_repository_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        baseRepository {{
                            id
                            databaseId
                            allowUpdateBranch
                            createdAt
                            archivedAt
                            autoMergeAllowed
                            visibility
                            forkCount
                            collaborators(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    bio
                                    avatarUrl
                                    createdAt
                                    email
                                    url
                                    websiteUrl
                                    userViewType
                                    estimatedNextSponsorsPayoutInCents
                                    commitComments {{
                                        totalCount
                                    }}
                                    company
                                    contributionsCollection {{
                                        commitContributionsByRepository {{
                                            url
                                            resourcePath
                                            contributions {{
                                                totalCount
                                            }}
                                            repository {{
                                                id
                                                databaseId
                                                name
                                                url
                                                sshUrl
                                                createdAt
                                                description
                                                isPrivate
                                                forkCount
                                                stargazerCount
                                                labels {{
                                                    totalCount
                                                }}
                                                languages {{
                                                    totalCount
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                        }}
                                    contributionCalendar {{
                                        colors
                                        isHalloween
                                        totalContributions
                                    }}
                                    contributionYears
                                    doesEndInCurrentMonth
                                    endedAt
                                    firstIssueContribution {{
                                        ... on CreatedIssueContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
                                            __typename
                                        }}
                                    }}
                                    firstPullRequestContribution {{
                                        ... on CreatedPullRequestContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
                                            __typename 
                                        }}
                                    }}
                                    firstRepositoryContribution {{
                                        ... on CreatedRepositoryContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url 
                                            __typename
                                        }}
                                    }}
                                    hasActivityInThePast
                                    hasAnyContributions
                                    hasAnyRestrictedContributions
                                    isSingleDay
                                    issueContributions {{
                                        totalCount
                                    }}
                                    issueContributionsByRepository {{
                                        repository {{
                                            id
                                            databaseId
                                            name
                                            url
                                            sshUrl
                                            createdAt
                                            description
                                            isPrivate
                                            forkCount
                                            stargazerCount
                                            labels {{
                                                totalCount
                                            }}
                                            languages {{
                                                totalCount
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions {{
                                            totalCount
                                        }}
                                    }}
                                    pullRequestContributions {{
                                        totalCount
                                    }}
                                    pullRequestContributionsByRepository {{
                                        repository {{
                                            id
                                            databaseId
                                            name
                                            url
                                            sshUrl
                                            createdAt
                                            description
                                            isPrivate
                                            forkCount
                                            stargazerCount
                                            labels {{
                                                totalCount
                                            }}
                                            languages {{
                                                totalCount
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions {{
                                            totalCount
                                        }}      
                                    }}
                                    pullRequestReviewContributions {{
                                        totalCount
                                    }}
                                    repositoryContributions {{
                                        totalCount
                                    }}
                                    startedAt
                                    totalCommitContributions
                                    totalIssueContributions
                                    totalPullRequestContributions
                                    totalPullRequestReviewContributions
                                    totalRepositoriesWithContributedCommits
                                    totalRepositoriesWithContributedIssues
                                    totalRepositoriesWithContributedPullRequestReviews
                                    totalRepositoriesWithContributedPullRequests
                                    totalRepositoryContributions
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(first: 100) {{
                                        totalCount
                                    }}
                                    gists {{
                                        totalCount
                                    }}
                                    hasSponsorsListing
                                    isBountyHunter
                                    isCampusExpert
                                    isDeveloperProgramMember
                                    isEmployee
                                    isGitHubStar
                                    isHireable
                                    isSiteAdmin
                                    issueComments {{
                                        totalCount
                                    }}
                                    issues{{
                                        totalCount
                                    }}
                                    lifetimeReceivedSponsorshipValues {{
                                        totalCount
                                    }}
                                    lists {{
                                        totalCount
                                    }}
                                    location
                                    login
                                    monthlyEstimatedSponsorsIncomeInCents
                                    name
                                    organizations{{
                                        totalCount
                                    }}
                                    packages {{
                                        totalCount
                                    }}
                                    projectsResourcePath
                                    projectsUrl
                                    pronouns
                                    pullRequests {{
                                        totalCount
                                    }}
                                    repositories {{
                                        totalCount
                                    }}
                                    repositoriesContributedTo {{
                                        totalCount
                                    }}
                                    repositoryDiscussionComments {{
                                        totalCount
                                    }}
                                    repositoryDiscussions{{
                                        totalCount
                                    }}
                                    socialAccounts {{
                                        totalCount
                                    }}
                                    sponsoring {{
                                        totalCount
                                    }}
                                    sponsors {{
                                        totalCount
                                    }}
                                    starredRepositories {{
                                        totalCount
                                        isOverLimit
                                    }}
                                    status {{
                                        id
                                        createdAt
                                        emoji
                                        expiresAt
                                        indicatesLimitedAvailability
                                        message
                                        updatedAt
                                    }}
                                    topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                        totalCount
                                    }}
                                    totalSponsorshipAmountAsSponsorInCents
                                    twitterUsername
                                    updatedAt  
                                    __typename
                                }} 
                            }}
                            commitComments {{
                                    totalCount
                            }}
                            contactLinks {{
                                name
                                url
                                about
                            }}
                            contributingGuidelines {{
                                body
                                resourcePath
                                url
                            }}
                            defaultBranchRef {{
                                id
                                name
                                prefix
                                target {{
                                    abbreviatedOid
                                    commitUrl
                                    id
                                    oid
                                    commitResourcePath
                                }}
                            }}
                            deleteBranchOnMerge
                            deployments {{
                                totalCount
                            }}
                            description
                            discussionCategories(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    createdAt
                                    description
                                    emoji
                                    isAnswerable
                                    name
                                    slug
                                    updatedAt
                                }}
                            }}
                            discussions(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    answerChosenAt
                                    body
                                    bodyText
                                    closed
                                    closedAt
                                    createdAt
                                    isAnswered
                                    labels {{
                                        totalCount
                                    }}
                                    category {{
                                        id
                                        name
                                        description
                                        emoji
                                        createdAt
                                    }}
                                    answer {{
                                        id
                                        databaseId
                                        body
                                        bodyText
                                        createdAt
                                        deletedAt
                                    }}
                                }}
                            }}
                            diskUsage
                            forkCount
                            forkingAllowed
                            forks(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    name
                                    url
                                    sshUrl
                                    createdAt
                                    description
                                    isPrivate
                                    forkCount
                                    stargazerCount
                                    labels {{
                                        totalCount
                                    }}
                                    languages {{
                                        totalCount
                                    }}
                                    primaryLanguage {{
                                        id
                                        color
                                        name
                                    }}
                                }}
                            }}
                            hasDiscussionsEnabled
                            hasIssuesEnabled
                            hasProjectsEnabled
                            hasPullRequestsEnabled
                            hasSponsorshipsEnabled
                            hasVulnerabilityAlertsEnabled
                            hasWikiEnabled
                            homepageUrl
                            isArchived
                            isBlankIssuesEnabled
                            isDisabled
                            isEmpty
                            isFork
                            isInOrganization
                            isLocked
                            isMirror
                            isPrivate
                            isSecurityPolicyEnabled
                            isTemplate
                            isUserConfigurationRepository
                            issueTemplates {{
                                name
                                title
                                body
                                about
                            }}
                            issueTypes(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    color
                                    description
                                    isEnabled
                                    name
                                }}
                            }}
                            issues {{
                                totalCount
                            }}
                            labels {{
                                totalCount
                            }}
                            languages {{
                                totalCount
                            }}
                            primaryLanguage {{
                                id
                                color
                                name
                            }}
                            latestRelease {{
                                id
                                databaseId
                                description
                                createdAt
                                author {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                immutable
                                isDraft
                                isLatest
                                isPrerelease
                                name
                                publishedAt
                                resourcePath
                                shortDescriptionHTML
                                updatedAt
                                url
                                tag {{
                                    id
                                    name
                                    prefix
                                }}
                                tagCommit {{
                                    id
                                    oid
                                    url
                                    message
                                    messageBody
                                    messageHeadline
                                    abbreviatedOid
                                    deletions
                                    additions
                                }}
                                tagName
                            }}
                            licenseInfo {{
                                id
                                body
                                description
                                name
                                nickname
                                url
                                spdxId
                            }}
                            lockReason
                            mergeCommitAllowed
                            mergeCommitMessage
                            mergeCommitTitle
                            milestones {{
                                totalCount
                            }}
                            mirrorUrl
                            name
                            nameWithOwner
                            openGraphImageUrl
                            owner {{
                                id
                                login
                                avatarUrl
                                resourcePath
                                url
                            }}
                            packages {{
                                totalCount
                            }}
                            parent {{
                                id
                                databaseId
                                name
                                url
                                sshUrl
                                createdAt
                                description
                                isPrivate
                                forkCount
                                stargazerCount
                                labels {{
                                    totalCount
                                }}
                                languages {{
                                    totalCount
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}
                            }}
                            projectsResourcePath
                            projectsUrl
                            pullRequestCreationPolicy
                            pullRequestTemplates {{
                                filename
                                body
                            }}
                            pullRequests {{
                                totalCount
                            }}
                            pushedAt
                            rebaseMergeAllowed
                            refs(refPrefix: "refs/heads/", first: 100) {{
                                totalCount
                            }}
                            releases(first: 100) {{
                                totalCount
                            }}
                            repositoryTopics(first: 100) {{
                                totalCount
                                nodes {{
                                   id
                                   resourcePath
                                   topic {{
                                       id
                                       name
                                       stargazerCount
                                   }}
                                    url 
                                }}
                            }}
                            resourcePath
                            rulesets {{
                                totalCount
                            }}
                            shortDescriptionHTML
                            squashMergeAllowed
                            squashMergeCommitMessage                      
                            squashMergeCommitTitle
                            sshUrl
                            stargazerCount
                            stargazers(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    createdAt
                                    login
                                    url
                                    __typename
                                }}
                            }}
                            submodules(first: 100) {{
                                totalCount
                                nodes {{
                                    branch
                                    name
                                    gitUrl
                                    path
                                    subprojectCommitOid
                                }}
                            }}
                            updatedAt
                            templateRepository {{    
                                id
                                databaseId
                                name
                                url
                                sshUrl
                                createdAt
                                description
                                isPrivate
                                forkCount
                                stargazerCount
                                labels {{
                                    totalCount
                                }}
                                languages {{
                                    totalCount
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}       
                            }}
                            url
                            watchers {{
                                totalCount
                            }}
                        }}
                        headRepository {{
                            id
                            databaseId
                            allowUpdateBranch
                            createdAt
                            archivedAt
                            autoMergeAllowed
                            visibility
                            forkCount
                            collaborators(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    bio
                                    avatarUrl
                                    createdAt
                                    email
                                    url
                                    websiteUrl
                                    userViewType
                                    estimatedNextSponsorsPayoutInCents
                                    commitComments {{
                                        totalCount
                                    }}
                                    company
                                    contributionsCollection {{
                                        commitContributionsByRepository {{
                                            url
                                            resourcePath
                                            contributions {{
                                                totalCount
                                            }}
                                            repository {{
                                                id
                                                databaseId
                                                name
                                                url
                                                sshUrl
                                                createdAt
                                                description
                                                isPrivate
                                                forkCount
                                                stargazerCount
                                                labels {{
                                                    totalCount
                                                }}
                                                languages {{
                                                    totalCount
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                        }}
                                    contributionCalendar {{
                                        colors
                                        isHalloween
                                        totalContributions
                                    }}
                                    contributionYears
                                    doesEndInCurrentMonth
                                    endedAt
                                    firstIssueContribution {{
                                        ... on CreatedIssueContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
                                            __typename
                                        }}
                                    }}
                                    firstPullRequestContribution {{
                                        ... on CreatedPullRequestContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
                                            __typename 
                                        }}
                                    }}
                                    firstRepositoryContribution {{
                                        ... on CreatedRepositoryContribution {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url 
                                            __typename
                                        }}
                                    }}
                                    hasActivityInThePast
                                    hasAnyContributions
                                    hasAnyRestrictedContributions
                                    isSingleDay
                                    issueContributions {{
                                        totalCount
                                    }}
                                    issueContributionsByRepository {{
                                        repository {{
                                            id
                                            databaseId
                                            name
                                            url
                                            sshUrl
                                            createdAt
                                            description
                                            isPrivate
                                            forkCount
                                            stargazerCount
                                            labels {{
                                                totalCount
                                            }}
                                            languages {{
                                                totalCount
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions {{
                                            totalCount
                                        }}
                                    }}
                                    pullRequestContributions {{
                                        totalCount
                                    }}
                                    pullRequestContributionsByRepository {{
                                        repository {{
                                            id
                                            databaseId
                                            name
                                            url
                                            sshUrl
                                            createdAt
                                            description
                                            isPrivate
                                            forkCount
                                            stargazerCount
                                            labels {{
                                                totalCount
                                            }}
                                            languages {{
                                                totalCount
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions {{
                                            totalCount
                                        }}      
                                    }}
                                    pullRequestReviewContributions {{
                                        totalCount
                                    }}
                                    repositoryContributions {{
                                        totalCount
                                    }}
                                    startedAt
                                    totalCommitContributions
                                    totalIssueContributions
                                    totalPullRequestContributions
                                    totalPullRequestReviewContributions
                                    totalRepositoriesWithContributedCommits
                                    totalRepositoriesWithContributedIssues
                                    totalRepositoriesWithContributedPullRequestReviews
                                    totalRepositoriesWithContributedPullRequests
                                    totalRepositoryContributions
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(first: 100) {{
                                        totalCount
                                    }}
                                    gists {{
                                        totalCount
                                    }}
                                    hasSponsorsListing
                                    isBountyHunter
                                    isCampusExpert
                                    isDeveloperProgramMember
                                    isEmployee
                                    isGitHubStar
                                    isHireable
                                    isSiteAdmin
                                    issueComments {{
                                        totalCount
                                    }}
                                    issues{{
                                        totalCount
                                    }}
                                    lifetimeReceivedSponsorshipValues {{
                                        totalCount
                                    }}
                                    lists {{
                                        totalCount
                                    }}
                                    location
                                    login
                                    monthlyEstimatedSponsorsIncomeInCents
                                    name
                                    organizations{{
                                        totalCount
                                    }}
                                    packages {{
                                        totalCount
                                    }}
                                    projectsResourcePath
                                    projectsUrl
                                    pronouns
                                    pullRequests {{
                                        totalCount
                                    }}
                                    repositories {{
                                        totalCount
                                    }}
                                    repositoriesContributedTo {{
                                        totalCount
                                    }}
                                    repositoryDiscussionComments {{
                                        totalCount
                                    }}
                                    repositoryDiscussions{{
                                        totalCount
                                    }}
                                    socialAccounts {{
                                        totalCount
                                    }}
                                    sponsoring {{
                                        totalCount
                                    }}
                                    sponsors {{
                                        totalCount
                                    }}
                                    starredRepositories {{
                                        totalCount
                                        isOverLimit
                                    }}
                                    status {{
                                        id
                                        createdAt
                                        emoji
                                        expiresAt
                                        indicatesLimitedAvailability
                                        message
                                        updatedAt
                                    }}
                                    topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                        totalCount
                                    }}
                                    totalSponsorshipAmountAsSponsorInCents
                                    twitterUsername
                                    updatedAt  
                                    __typename
                                }} 
                            }}
                            commitComments {{
                                    totalCount
                            }}
                            contactLinks {{
                                name
                                url
                                about
                            }}
                            contributingGuidelines {{
                                body
                                resourcePath
                                url
                            }}
                            defaultBranchRef {{
                                id
                                name
                                prefix
                                target {{
                                    abbreviatedOid
                                    commitUrl
                                    id
                                    oid
                                    commitResourcePath
                                }}
                            }}
                            deleteBranchOnMerge
                            deployments {{
                                totalCount
                            }}
                            description
                            discussionCategories(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    createdAt
                                    description
                                    emoji
                                    isAnswerable
                                    name
                                    slug
                                    updatedAt
                                }}
                            }}
                            discussions(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    answerChosenAt
                                    body
                                    bodyText
                                    closed
                                    closedAt
                                    createdAt
                                    isAnswered
                                    labels {{
                                        totalCount
                                    }}
                                    category {{
                                        id
                                        name
                                        description
                                        emoji
                                        createdAt
                                    }}
                                    answer {{
                                        id
                                        databaseId
                                        body
                                        bodyText
                                        createdAt
                                        deletedAt
                                    }}
                                }}
                            }}
                            diskUsage
                            forkCount
                            forkingAllowed
                            forks(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    name
                                    url
                                    sshUrl
                                    createdAt
                                    description
                                    isPrivate
                                    forkCount
                                    stargazerCount
                                    labels {{
                                        totalCount
                                    }}
                                    languages {{
                                        totalCount
                                    }}
                                    primaryLanguage {{
                                        id
                                        color
                                        name
                                    }}
                                }}
                            }}
                            hasDiscussionsEnabled
                            hasIssuesEnabled
                            hasProjectsEnabled
                            hasPullRequestsEnabled
                            hasSponsorshipsEnabled
                            hasVulnerabilityAlertsEnabled
                            hasWikiEnabled
                            homepageUrl
                            isArchived
                            isBlankIssuesEnabled
                            isDisabled
                            isEmpty
                            isFork
                            isInOrganization
                            isLocked
                            isMirror
                            isPrivate
                            isSecurityPolicyEnabled
                            isTemplate
                            isUserConfigurationRepository
                            issueTemplates {{
                                name
                                title
                                body
                                about
                            }}
                            issueTypes(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    color
                                    description
                                    isEnabled
                                    name
                                }}
                            }}
                            issues {{
                                totalCount
                            }}
                            labels {{
                                totalCount
                            }}
                            languages {{
                                totalCount
                            }}
                            primaryLanguage {{
                                id
                                color
                                name
                            }}
                            latestRelease {{
                                id
                                databaseId
                                description
                                createdAt
                                author {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                immutable
                                isDraft
                                isLatest
                                isPrerelease
                                name
                                publishedAt
                                resourcePath
                                shortDescriptionHTML
                                updatedAt
                                url
                                tag {{
                                    id
                                    name
                                    prefix
                                }}
                                tagCommit {{
                                    id
                                    oid
                                    url
                                    message
                                    messageBody
                                    messageHeadline
                                    abbreviatedOid
                                    deletions
                                    additions
                                }}
                                tagName
                            }}
                            licenseInfo {{
                                id
                                body
                                description
                                name
                                nickname
                                url
                                spdxId
                            }}
                            lockReason
                            mergeCommitAllowed
                            mergeCommitMessage
                            mergeCommitTitle
                            milestones {{
                                totalCount
                            }}
                            mirrorUrl
                            name
                            nameWithOwner
                            openGraphImageUrl
                            owner {{
                                id
                                login
                                avatarUrl
                                resourcePath
                                url
                            }}
                            packages {{
                                totalCount
                            }}
                            parent {{
                                id
                                databaseId
                                name
                                url
                                sshUrl
                                createdAt
                                description
                                isPrivate
                                forkCount
                                stargazerCount
                                labels {{
                                    totalCount
                                }}
                                languages {{
                                    totalCount
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}
                            }}
                            projectsResourcePath
                            projectsUrl
                            pullRequestCreationPolicy
                            pullRequestTemplates {{
                                filename
                                body
                            }}
                            pullRequests {{
                                totalCount
                            }}
                            pushedAt
                            rebaseMergeAllowed
                            refs(refPrefix: "refs/heads/", first: 100) {{
                                totalCount
                            }}
                            releases(first: 100) {{
                                totalCount
                            }}
                            repositoryTopics(first: 100) {{
                                totalCount
                                nodes {{
                                   id
                                   resourcePath
                                   topic {{
                                       id
                                       name
                                       stargazerCount
                                   }}
                                    url 
                                }}
                            }}
                            resourcePath
                            rulesets {{
                                totalCount
                            }}
                            shortDescriptionHTML
                            squashMergeAllowed
                            squashMergeCommitMessage                      
                            squashMergeCommitTitle
                            sshUrl
                            stargazerCount
                            stargazers(first: 100) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    createdAt
                                    login
                                    url
                                    __typename
                                }}
                            }}
                            submodules(first: 100) {{
                                totalCount
                                nodes {{
                                    branch
                                    name
                                    gitUrl
                                    path
                                    subprojectCommitOid
                                }}
                            }}
                            updatedAt
                            templateRepository {{    
                                id
                                databaseId
                                name
                                url
                                sshUrl
                                createdAt
                                description
                                isPrivate
                                forkCount
                                stargazerCount
                                labels {{
                                    totalCount
                                }}
                                languages {{
                                    totalCount
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}       
                            }}
                            url
                            watchers {{
                                totalCount
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query



# Get user information from each PR, based on the PR IDs already collected.   
def pr_user_query(self, pr_ids: str) -> str:
        query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fullDatabaseId
                        editor {{
                            login
                            url
                            avatarUrl
                            __typename
                        }}
                        assignedActors(first: 100) {{
                            totalCount
                            nodes {{
                                ... on Bot {{
                                    id
                                    databaseId
                                    login 
                                    url
                                    createdAt
                                    updatedAt 
                                    avatarUrl 
                                    resourcePath
                                    __typename 
                                }}
                                ... on Mannequin {{
                                    id
                                    databaseId
                                    name 
                                    login
                                    email
                                    url 
                                    createdAt
                                    updatedAt
                                    resourcePath
                                    claimant {{
                                        id
                                        databaseId
                                        login 
                                        email
                                        url
                                        __typename   
                                    }}
                                    __typename
                                }}
                                ... on Organization {{
                                    id
                                    databaseId
                                    email
                                    login
                                    location
                                    description
                                    createdAt
                                    archivedAt
                                    avatarUrl
                                    teams(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            databaseId
                                            description
                                            avatarUrl
                                            childTeams {{
                                                totalCount
                                            }}
                                            ancestors {{
                                                totalCount
                                            }}
                                            members {{
                                                totalCount
                                            }}
                                            membersUrl
                                            name
                                            privacy
                                            combinedSlug
                                            createdAt                                            
                                        }}
                                    }}
                                    teamsResourcePath
                                    domains(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            databaseId
                                            domain
                                            dnsHostName
                                            isApproved
                                            isRequiredForPolicyEnforcement
                                            isVerified
                                            updatedAt
                                            owner {{                                                 __typename                                             }}
                                            verificationToken 
                                        }}
                                    }}
                                    hasSponsorsListing
                                    isSponsoringViewer
                                    isVerified
                                    issueFields {{
                                        totalCount
                                    }}
                                    issueTypes {{
                                        totalCount
                                    }}
                                    lifetimeReceivedSponsorshipValues {{
                                      totalCount
                                    }}
                                    mannequins {{
                                      totalCount
                                    }}
                                    memberStatuses(first: 100) {{ 
                                        totalCount
                                        nodes {{
                                            id
                                            message
                                            indicatesLimitedAvailability 
                                            emoji 
                                            createdAt
                                            expiresAt
                                            updatedAt    
                                        }}
                                    }}
                                    membersCanForkPrivateRepositories
                                    membersWithRole(first: 100) {{
                                      totalCount
                                      nodes {{
                                          id
                                          databaseId
                                          login
                                          name
                                          location                                          
                                          email
                                          bio
                                          url
                                          pronouns
                                          avatarUrl 
                                          company 
                                          createdAt
                                          commitComments {{
                                              totalCount                                            
                                          }}
                                          followers {{
                                              totalCount
                                          }}
                                          following {{
                                              totalCount
                                          }}
                                          gists {{
                                              totalCount
                                          }}
                                        hasSponsorsListing
                                        isBountyHunter
                                        isCampusExpert
                                        isDeveloperProgramMember
                                        isEmployee
                                        isGitHubStar
                                        isHireable
                                        isSiteAdmin
                                        isSponsoringViewer
                                        isViewer
                                        issueComments {{
                                            totalCount
                                        }}
                                        issues {{
                                            totalCount
                                        }}
                                        lists {{
                                            totalCount 
                                        }}
                                        monthlyEstimatedSponsorsIncomeInCents
                                        organizations {{
                                            totalCount
                                        }}
                                        packages {{
                                            totalCount
                                        }}
                                        projectsResourcePath
                                        projectsUrl
                                        pullRequests {{
                                            totalCount
                                        }}
                                        recentProjects {{
                                            totalCount
                                        }}
                                        repositoriesContributedTo {{
                                            totalCount
                                        }}
                                        repositoryDiscussionComments {{
                                            totalCount
                                        }}
                                        resourcePath
                                        socialAccounts {{
                                            totalCount
                                        }}
                                        sponsoring {{
                                            totalCount
                                        }}
                                        sponsors {{
                                            totalCount
                                        }}
                                        starredRepositories {{
                                            totalCount
                                        }}
                                        status {{
                                            id
                                            emoji
                                            message
                                            createdAt
                                            updatedAt
                                            expiresAt
                                        }}
                                        topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt
                                        userViewType
                                        watching {{
                                            totalCount
                                        }}
                                        websiteUrl
                                        __typename  
                                        }}
                                    }}
                                    __typename
                                }}
                                
                                ... on User {{
                                          id
                                          databaseId
                                          login
                                          name
                                          location                                          
                                          email
                                          bio
                                          url
                                          pronouns
                                          avatarUrl 
                                          company 
                                          createdAt
                                          commitComments {{
                                              totalCount                                            
                                          }}
                                          followers {{
                                              totalCount
                                          }}
                                          following {{
                                              totalCount
                                          }}
                                          gists {{
                                              totalCount
                                          }}
                                        hasSponsorsListing
                                        isBountyHunter
                                        isCampusExpert
                                        isDeveloperProgramMember
                                        isEmployee
                                        isGitHubStar
                                        isHireable
                                        isSiteAdmin
                                        isSponsoringViewer
                                        isViewer
                                        issueComments {{
                                            totalCount
                                        }}
                                        issues {{
                                            totalCount
                                        }}
                                        lists {{
                                            totalCount 
                                        }}
                                        monthlyEstimatedSponsorsIncomeInCents
                                        organizations {{
                                            totalCount
                                        }}
                                        packages {{
                                            totalCount
                                        }}
                                        projectsResourcePath
                                        projectsUrl
                                        pullRequests {{
                                            totalCount
                                        }}
                                        recentProjects {{
                                            totalCount
                                        }}
                                        repositoriesContributedTo {{
                                            totalCount
                                        }}
                                        repositoryDiscussionComments {{
                                            totalCount
                                        }}
                                        resourcePath
                                        socialAccounts {{
                                            totalCount
                                        }}
                                        sponsoring {{
                                            totalCount
                                        }}
                                        sponsors {{
                                            totalCount
                                        }}
                                        starredRepositories {{
                                            totalCount
                                        }}
                                        status {{
                                            id
                                            emoji
                                            message
                                            createdAt
                                            updatedAt
                                            expiresAt
                                        }}
                                        topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt
                                        userViewType
                                        watching {{
                                            totalCount
                                        }}
                                        websiteUrl
                                        __typename  
                                    }}
                                }}
                            }}
                            author {{
                               ... on Bot {{
                                    id
                                    databaseId
                                    login 
                                    url
                                    createdAt
                                    updatedAt 
                                    avatarUrl 
                                    resourcePath
                                    __typename 
                               }}
                               ... on Mannequin {{
                                    id
                                    databaseId
                                    name 
                                    login
                                    email
                                    url 
                                    createdAt
                                    updatedAt
                                    resourcePath
                                    claimant {{
                                        id
                                        databaseId
                                        createdAt
                                        login 
                                        email
                                        url
                                        __typename   
                                    }}
                                    __typename
                               }}
                               ... on Organization {{
                                    id
                                    databaseId
                                    email
                                    login
                                    location
                                    description
                                    createdAt
                                    archivedAt
                                    avatarUrl
                                    teams(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            databaseId
                                            description
                                            avatarUrl
                                            childTeams {{
                                                totalCount
                                            }}
                                            ancestors {{
                                                totalCount
                                            }}
                                            members {{
                                                totalCount
                                            }}
                                            membersUrl
                                            name
                                            privacy
                                            combinedSlug
                                            createdAt                                            
                                        }}
                                    }}
                                    teamsResourcePath
                                    domains(first: 100) {{
                                        totalCount
                                        nodes {{
                                            id
                                            databaseId
                                            domain
                                            dnsHostName
                                            isApproved
                                            isRequiredForPolicyEnforcement
                                            isVerified
                                            updatedAt
                                            owner {{                                                 __typename                                             }}
                                            verificationToken 
                                        }}
                                    }}
                                    hasSponsorsListing
                                    isSponsoringViewer
                                    isVerified
                                    issueFields{{
                                        totalCount                                      
                                    }}
                                    issueTypes {{
                                        totalCount
                                    }}
                                    lifetimeReceivedSponsorshipValues {{
                                      totalCount
                                    }}
                                    mannequins {{
                                      totalCount 
                                    }}
                                    memberStatuses(first: 100) {{ 
                                        totalCount
                                        nodes {{
                                            id
                                            message
                                            indicatesLimitedAvailability 
                                            emoji 
                                            createdAt
                                            expiresAt
                                            updatedAt    
                                        }}
                                    }}
                                    membersCanForkPrivateRepositories
                                    membersWithRole(first: 100) {{
                                      totalCount
                                      nodes {{
                                          id
                                          databaseId
                                          login
                                          name
                                          location                                          
                                          email
                                          bio
                                          url
                                          pronouns
                                          avatarUrl 
                                          company 
                                          createdAt
                                          commitComments {{
                                              totalCount                                            
                                          }}
                                          followers {{
                                              totalCount
                                          }}
                                          following {{
                                              totalCount
                                          }}
                                          gists {{
                                              totalCount
                                          }}
                                          hasSponsorsListing
                                          hovercard {{
                                            contexts {{
                                                message
                                                octicon
                                            }}
                                        }}
                                        isBountyHunter
                                        isCampusExpert
                                        isDeveloperProgramMember
                                        isEmployee
                                        isGitHubStar
                                        isHireable
                                        isSiteAdmin
                                        isSponsoringViewer
                                        isViewer
                                        issueComments {{
                                            totalCount
                                        }}
                                        issues {{
                                            totalCount
                                        }}
                                        lists {{
                                            totalCount 
                                        }}
                                        monthlyEstimatedSponsorsIncomeInCents
                                        organizations {{
                                            totalCount
                                        }}
                                        packages {{
                                            totalCount
                                        }}
                                        projectsResourcePath
                                        projectsUrl
                                        pullRequests {{
                                            totalCount
                                        }}
                                        recentProjects {{
                                            totalCount
                                        }}
                                        repositoriesContributedTo {{
                                            totalCount
                                        }}
                                        repositoryDiscussionComments {{
                                            totalCount
                                        }}
                                        resourcePath
                                        socialAccounts {{
                                            totalCount
                                        }}
                                        sponsoring {{
                                            totalCount
                                        }}
                                        sponsors {{
                                            totalCount
                                        }}
                                        starredRepositories {{
                                            totalCount
                                        }}
                                        status {{
                                            id
                                            emoji
                                            message
                                            createdAt
                                            updatedAt
                                            expiresAt
                                        }}
                                        topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt
                                        userViewType
                                        watching {{
                                            totalCount
                                        }}
                                        websiteUrl
                                        __typename  
                                        }}
                                    }}
                                    __typename
                             }}
                               ... on EnterpriseUserAccount {{
                                   id
                                   login
                                   name
                                   url
                                   resourcePath
                                   avatarUrl
                                   createdAt
                                   updatedAt
                                   enterprise {{
                                       id
                                       databaseId
                                       avatarUrl
                                       name
                                       billingEmail
                                       createdAt
                                       description
                                       location
                                       members {{
                                           totalCount
                                       }}
                                       organizations {{
                                           totalCount
                                       }}
                                       readme
                                       resourcePath
                                       slug
                                       securityContactEmail
                                       websiteUrl                                              
                                   }}
                                   user {{
                                        id
                                        databaseId
                                        bio
                                        avatarUrl
                                        createdAt
                                        email
                                        url
                                        websiteUrl
                                        userViewType
                                        estimatedNextSponsorsPayoutInCents
                                        commitComments {{
                                            totalCount
                                        }}
                                        company
                                        contributionsCollection {{
                                            commitContributionsByRepository {{
                                                url
                                                resourcePath
                                                contributions {{
                                                    totalCount
                                                }}
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                            }}
                                            contributionCalendar {{
                                                colors
                                                isHalloween
                                                totalContributions
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
                                                    __typename
                                                }}
                                            }}
                                            firstPullRequestContribution {{
                                                ... on CreatedPullRequestContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
                                                    __typename 
                                                }}
                                            }}
                                            firstRepositoryContribution {{
                                                ... on CreatedRepositoryContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url 
                                                    __typename
                                                }}
                                            }}
                                            hasActivityInThePast
                                            hasAnyContributions
                                            hasAnyRestrictedContributions
                                            isSingleDay
                                            issueContributions {{
                                                totalCount
                                            }}
                                            issueContributionsByRepository {{
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions {{
                                                totalCount
                                            }}
                                            pullRequestContributionsByRepository {{
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions {{
                                                    totalCount
                                                }}      
                                            }}
                                            pullRequestReviewContributions {{
                                                totalCount
                                            }}
                                            repositoryContributions {{
                                                totalCount
                                            }}
                                            startedAt
                                            totalCommitContributions
                                            totalIssueContributions
                                            totalPullRequestContributions
                                            totalPullRequestReviewContributions
                                            totalRepositoriesWithContributedCommits
                                            totalRepositoriesWithContributedIssues
                                            totalRepositoriesWithContributedPullRequestReviews
                                            totalRepositoriesWithContributedPullRequests
                                            totalRepositoryContributions
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(first: 100) {{
                                            totalCount
                                        }}
                                        gists {{
                                            totalCount
                                        }}
                                        hasSponsorsListing
                                        isBountyHunter
                                        isCampusExpert
                                        isDeveloperProgramMember
                                        isEmployee
                                        isGitHubStar
                                        isHireable
                                        isSiteAdmin
                                        issueComments {{
                                            totalCount
                                        }}
                                        issues{{
                                            totalCount
                                        }}
                                        lifetimeReceivedSponsorshipValues {{
                                            totalCount
                                        }}
                                        lists {{
                                            totalCount
                                        }}
                                        location
                                        login
                                        monthlyEstimatedSponsorsIncomeInCents
                                        name
                                        organizations{{
                                            totalCount
                                        }}
                                        packages {{
                                            totalCount
                                        }}
                                        projectsResourcePath
                                        projectsUrl
                                        pronouns
                                        pullRequests {{
                                            totalCount
                                        }}
                                        repositories {{
                                            totalCount
                                        }}
                                        repositoriesContributedTo {{
                                            totalCount
                                        }}
                                        repositoryDiscussionComments {{
                                            totalCount
                                        }}
                                        repositoryDiscussions{{
                                            totalCount
                                        }}
                                        socialAccounts {{
                                            totalCount
                                        }}
                                        sponsoring {{
                                            totalCount
                                        }}
                                        sponsors {{
                                            totalCount
                                        }}
                                        starredRepositories {{
                                            totalCount
                                            isOverLimit
                                        }}
                                        status {{
                                            id
                                            createdAt
                                            emoji
                                            expiresAt
                                            indicatesLimitedAvailability
                                            message
                                            updatedAt
                                        }}
                                        topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt  
                                        __typename
                                    }}
                                }}
                                ... on User {{
                                        id
                                        databaseId
                                        bio
                                        avatarUrl
                                        createdAt
                                        email
                                        url
                                        websiteUrl
                                        userViewType
                                        estimatedNextSponsorsPayoutInCents
                                        commitComments {{
                                            totalCount
                                        }}
                                        company
                                        contributionsCollection {{
                                            commitContributionsByRepository {{
                                                url
                                                resourcePath
                                                contributions {{
                                                    totalCount
                                                }}
                                                repository {{
                                                    id
                                                    databaseId
                                                    name
                                                    url
                                                    sshUrl
                                                    createdAt
                                                    description
                                                    isPrivate
                                                    forkCount
                                                    stargazerCount
                                                    labels {{
                                                        totalCount
                                                    }}
                                                    languages {{
                                                        totalCount
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                            }}
                                        contributionCalendar {{
                                            colors
                                            isHalloween
                                            totalContributions
                                        }}
                                        contributionYears
                                        doesEndInCurrentMonth
                                        endedAt
                                        firstIssueContribution {{
                                            ... on CreatedIssueContribution {{
                                                isRestricted
                                                occurredAt
                                                resourcePath
                                                url
                                                __typename
                                            }}
                                        }}
                                        firstPullRequestContribution {{
                                            ... on CreatedPullRequestContribution {{
                                                isRestricted
                                                occurredAt
                                                resourcePath
                                                url
                                                __typename 
                                            }}
                                        }}
                                        firstRepositoryContribution {{
                                            ... on CreatedRepositoryContribution {{
                                                isRestricted
                                                occurredAt
                                                resourcePath
                                                url 
                                                __typename
                                            }}
                                        }}
                                        hasActivityInThePast
                                        hasAnyContributions
                                        hasAnyRestrictedContributions
                                        isSingleDay
                                        issueContributions {{
                                            totalCount
                                        }}
                                        issueContributionsByRepository {{
                                            repository {{
                                                id
                                                databaseId
                                                name
                                                url
                                                sshUrl
                                                createdAt
                                                description
                                                isPrivate
                                                forkCount
                                                stargazerCount
                                                labels {{
                                                    totalCount
                                                }}
                                                languages {{
                                                    totalCount
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                            contributions {{
                                                totalCount
                                            }}
                                        }}
                                        pullRequestContributions {{
                                            totalCount
                                        }}
                                        pullRequestContributionsByRepository {{
                                            repository {{
                                                id
                                                databaseId
                                                name
                                                url
                                                sshUrl
                                                createdAt
                                                description
                                                isPrivate
                                                forkCount
                                                stargazerCount
                                                labels {{
                                                    totalCount
                                                }}
                                                languages {{
                                                    totalCount
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                            contributions {{
                                                totalCount
                                            }}      
                                        }}
                                        pullRequestReviewContributions {{
                                            totalCount
                                        }}
                                        repositoryContributions {{
                                            totalCount
                                        }}
                                        startedAt
                                        totalCommitContributions
                                        totalIssueContributions
                                        totalPullRequestContributions
                                        totalPullRequestReviewContributions
                                        totalRepositoriesWithContributedCommits
                                        totalRepositoriesWithContributedIssues
                                        totalRepositoriesWithContributedPullRequestReviews
                                        totalRepositoriesWithContributedPullRequests
                                        totalRepositoryContributions
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(first: 100) {{
                                        totalCount
                                    }}
                                    gists {{
                                        totalCount
                                    }}
                                    hasSponsorsListing
                                    isBountyHunter
                                    isCampusExpert
                                    isDeveloperProgramMember
                                    isEmployee
                                    isGitHubStar
                                    isHireable
                                    isSiteAdmin
                                    issueComments {{
                                        totalCount
                                    }}
                                    issues{{
                                        totalCount
                                    }}
                                    lifetimeReceivedSponsorshipValues {{
                                        totalCount
                                    }}
                                    lists {{
                                        totalCount
                                    }}
                                    location
                                    login
                                    monthlyEstimatedSponsorsIncomeInCents
                                    name
                                    organizations{{
                                        totalCount
                                    }}
                                    packages {{
                                        totalCount
                                    }}
                                    projectsResourcePath
                                    projectsUrl
                                    pronouns
                                    pullRequests {{
                                        totalCount
                                    }}
                                    repositories {{
                                        totalCount
                                    }}
                                    repositoriesContributedTo {{
                                        totalCount
                                    }}
                                    repositoryDiscussionComments {{
                                        totalCount
                                    }}
                                    repositoryDiscussions{{
                                        totalCount
                                    }}
                                    socialAccounts {{
                                        totalCount
                                    }}
                                    sponsoring {{
                                        totalCount
                                    }}
                                    sponsors {{
                                        totalCount
                                    }}
                                    starredRepositories {{
                                        totalCount
                                        isOverLimit
                                    }}
                                    status {{
                                        id
                                        createdAt
                                        emoji
                                        expiresAt
                                        indicatesLimitedAvailability
                                        message
                                        updatedAt
                                    }}
                                    topRepositories(orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                                        totalCount
                                    }}
                                    totalSponsorshipAmountAsSponsorInCents
                                    twitterUsername
                                    updatedAt  
                                    __typename
                                }}
                                __typename
                                }}
                                editor {{
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                mergedBy {{
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                participants(first: 100) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        avatarUrl
                                        createdAt
                                        login
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                }}
                                suggestedActors(first: 100) {{
                                    totalCount
                                    nodes {{
                                        __typename
                                    }}
                                }}
                                suggestedReviewerActors(first: 100) {{
                                    totalCount
                                    nodes {{
                                        isAuthor
                                        isCommenter
                                        reviewer {{
                                            login
                                            avatarUrl
                                            resourcePath
                                            url 
                                        }}
                                    }}
                                }}
                                suggestedReviewers {{
                                    isAuthor
                                    isCommenter
                                    reviewer {{
                                        login
                                        avatarUrl
                                        resourcePath
                                        url 
                                    }}
                                }}
                            }}
                        }}
                    }}          
                """
        return query


def _after_arg(after: Optional[str]) -> str:
    return f', after: "{after}"' if after else ""


# Follow-up query for repository labels. Use repository IDs collected by the
# main PR/repository queries and paginate this separately.
def repository_labels_query(self, repository_ids: str, first: int = 100, after: Optional[str] = None) -> str:
    query = f"""
            query {{
                nodes(ids: [{repository_ids}]) {{
                    ... on Repository {{
                        id
                        databaseId
                        name
                        nameWithOwner
                        labels(first: {first}{_after_arg(after)}) {{
                            totalCount
                            pageInfo {{
                                endCursor
                                hasNextPage
                            }}
                            nodes {{
                                id
                                name
                                color
                                description
                                createdAt
                                isDefault
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query


# Follow-up query for repository languages. Use this separately from repository
# metadata queries so language nodes do not multiply inside nested PR/user paths.
def repository_languages_query(self, repository_ids: str, first: int = 100, after: Optional[str] = None) -> str:
    query = f"""
            query {{
                nodes(ids: [{repository_ids}]) {{
                    ... on Repository {{
                        id
                        databaseId
                        name
                        nameWithOwner
                        languages(first: {first}{_after_arg(after)}) {{
                            totalCount
                            totalSize
                            pageInfo {{
                                endCursor
                                hasNextPage
                            }}
                            edges {{
                                size
                                node {{
                                    id
                                    color
                                    name
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query


# Follow-up query for user top repositories. Use user IDs collected from PR
# authors, commenters, reviewers, assignees, or participants.
def user_top_repositories_query(self, user_ids: str, first: int = 100, after: Optional[str] = None) -> str:
    query = f"""
            query {{
                nodes(ids: [{user_ids}]) {{
                    ... on User {{
                        id
                        databaseId
                        login
                        topRepositories(first: {first}{_after_arg(after)}, orderBy: {{field: UPDATED_AT, direction: DESC}}) {{
                            totalCount
                            pageInfo {{
                                endCursor
                                hasNextPage
                            }}
                            nodes {{
                                id
                                databaseId
                                name
                                nameWithOwner
                                url
                                sshUrl
                                createdAt
                                description
                                isPrivate
                                forkCount
                                stargazerCount
                                labels {{
                                    totalCount
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query


# Follow-up query for user contributions by repository. This keeps contribution
# nodes out of the main PR queries, avoiding GitHub's 500k possible-node cap.
def user_contributions_by_repository_query(
    self,
    user_ids: str,
    first: int = 100,
    after: Optional[str] = None,
) -> str:
    query = f"""
            query {{
                nodes(ids: [{user_ids}]) {{
                    ... on User {{
                        id
                        databaseId
                        login
                        contributionsCollection {{
                            commitContributionsByRepository {{
                                repository {{
                                    id
                                    databaseId
                                    name
                                    nameWithOwner
                                    url
                                    labels {{
                                        totalCount
                                    }}
                                }}
                                contributions(first: {first}{_after_arg(after)}) {{
                                    totalCount
                                    pageInfo {{
                                        endCursor
                                        hasNextPage
                                    }}
                                    nodes {{
                                        isRestricted
                                        occurredAt
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                }}
                            }}
                            issueContributionsByRepository {{
                                repository {{
                                    id
                                    databaseId
                                    name
                                    nameWithOwner
                                    url
                                    labels {{
                                        totalCount
                                    }}
                                }}
                                contributions(first: {first}{_after_arg(after)}) {{
                                    totalCount
                                    pageInfo {{
                                        endCursor
                                        hasNextPage
                                    }}
                                    nodes {{
                                        isRestricted
                                        occurredAt
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                }}
                            }}
                            pullRequestContributionsByRepository {{
                                repository {{
                                    id
                                    databaseId
                                    name
                                    nameWithOwner
                                    url
                                    labels {{
                                        totalCount
                                    }}
                                }}
                                contributions(first: {first}{_after_arg(after)}) {{
                                    totalCount
                                    pageInfo {{
                                        endCursor
                                        hasNextPage
                                    }}
                                    nodes {{
                                        isRestricted
                                        occurredAt
                                        resourcePath
                                        url
                                        __typename
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        """
    return query
