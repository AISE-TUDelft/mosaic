
# Collect initial information about each PR
# Should scrape from January 1st 2023 until current date.
# after parameter was initially used for pagination, but no longer needed if you handle pagination internally
# Similarly, you can remove the filter parameter within the search, it was initially used to get PRs for a certain agent. Now we want to collect ALL PRs, irrespective of the authorship. We'll perform the filtering afterwards.
def backbone_pr_query(filter:str, start_date:str, end_date:str, first: int, after: Optional[str]) -> str:
        query = f"""
            query {{
                search(type: ISSUE, query:"is:pr {filter} created:{start_date}..{end_date} sort:created-asc", first: {first}, after: {f'"{after}"' if after else 'null'}) {{
                    issueCount
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                    nodes {{
                        ... on PullRequest {{
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
                            canbeRebased
                            changedFiles
                            additions
                            deletions
                            activeLockReason
                            createdViaEmail
                            includesCreatedEdit
                            maintainerCanModify
                            checksResourcePath
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
                            autoMergeRequest {{
                                authorEmail
                                commitBody
                                commitHeadLine
                                enabledAt
                                mergeMethod
                            }}
                            files(handle_pagination) {{
                                totalCount
                                nodes {{
                                    additions
                                    deletions
                                    changeType
                                    path
                                }}
                            }}
                            labels(handle_pagination) {{
                                totalCount
                                nodes {{
                                    name 
                                    color
                                    description
                                    createdAt
                                    isDefault
                                }}
                            }}
                            mergedBy {{
                                id
                                databaseId
                                createdAt
                                avatarUrl
                                login
                                resourcePath
                                url
                                __typename
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
                            participants(handle_pagination) {{
                                totalCount
                                nodes {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename
                                }}
                            }}
                            reactionGroups {{
                                createdAt
                                content
                                subject {{
                                    databaseId
                                    id  
                                }}
                            }}
                            reactions(handle_pagination) {{
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
                            timelineItems(handle_pagination) {{
                                totalCount
                                filteredCount
                                updatedAt
                                nodes {{
                                    id
                                    createdAt
                                    __typename
                                }}
                            }}
                        }}
                    }}
                }}            
            }} 
        """
        return query  
    


# Get review information from each PR, based on the PR IDs already collected.
def pr_review_query(self, pr_ids: str) -> str: 
    query = f"""
            query {{
                nodes(ids: [{pr_ids}]) {{
                    ... on PullRequest {{
                        id
                        fulldatabaseId
                        reviewRequests(handle_pagination) {{
                            totalCount
                            nodes {{
                                id
                                databaseId
                                asCodeOwner
                                requestedReviewer {{
                                    id
                                    databaseId
                                    login
                                    avatarUrl
                                    url
                                    __typename
                                }}
                            }}
                        }}
                        reviewThreads(handle_pagination) {{
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
                                        id
                                        databaseId
                                        login
                                        name
                                        avatarUrl
                                        url
                                        __typename
                                    }}
                                subjectType 
                            }}  
                        }}
                        reviews(handle_pagination) {{
                                totalCount
                                nodes {{
                                    id
                                    fullDatabaseId
                                    authorAssociation
                                    authors {{
                                        id
                                        databaseId
                                        createdAt
                                        avatarUrl
                                        login
                                        resourcePath
                                        url
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
                                                    contributions(handle_pagination) {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                                months
                                                totalContributions
                                                weeks
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resorucePath
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions(handle_pagination) {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                            pullRequestReviewContributionsByRepository(handle_pagination) {{
                                                totalCount
                                                nodes {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                            }}
                                            repositoryContributions(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                }}
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
                                        enterprises {{
                                            totalCount
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(handle_pagination) {{
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
                                        isSponsoredBy
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
                                        topRepositories(handle_pagination) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt  
                                        __typename
                                        }} 
                                    }}
                                    body
                                    bodyText
                                    createdAt
                                    editor {{
                                        id
                                        databaseId
                                        createdAt
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
                                        reactors(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                id
                                                databaseId
                                                login
                                                url
                                                __typename  
                                            }}
                                        }}
                                    }}
                                    reactions(handle_pagination) {{
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
                                comments(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
                                    }}
                                    languages(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            color
                                            id
                                            name
                                        }}
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
                        fulldatabaseId
                        mergeCommit {{
                            id
                            oid
                            url
                            message
                            messageBody
                            messageHeadLine
                            abbreviatedOid
                            additions
                            associatedPullRequests(handle_pagination) {{
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
                                    canbeRebased
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
                                id
                                databaseId
                                createdAt
                                avatarUrl
                                login
                                resourcePath
                                url
                                __typename
                            }}
                            committer {{
                                id
                                databaseId
                                createdAt
                                avatarUrl
                                login
                                resourcePath
                                url
                                __typename
                            }}
                        }}
                        commits(handle_pagination) {{
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
                                    associatedPullRequests(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            id
                                            fullDatabaseId
                                        }}
                                    }}
                                    author {{
                                        id
                                        databaseId
                                        createdAt
                                        avatarUrl
                                        email
                                        name
                                        login
                                        __typename 
                                    }}
                                    authoredByCommitter
                                    authoredDate
                                    changedFilesIfAvailable
                                    authors(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            avatarUrl
                                            email
                                            name
                                            login
                                            createdAt
                                            __typename
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
                                                        contributions(handle_pagination) {{
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
                                                            labels(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    name 
                                                                    color
                                                                    description
                                                                    createdAt
                                                                    isDefault
                                                                }}
                                                            }}
                                                            languages(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    color
                                                                    id
                                                                    name
                                                                }}
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
                                                    months
                                                    totalContributions
                                                    weeks
                                                }}
                                                contributionYears
                                                doesEndInCurrentMonth
                                                endedAt
                                                firstIssueContribution {{
                                                    ... on CreatedIssueContribution {{
                                                        isRestricted
                                                        occurredAt
                                                        resorucePath
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                    contributions(handle_pagination) {{
                                                        totalCount
                                                    }}
                                                }}
                                                pullRequestContributions(handle_pagination) {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                                pullRequestReviewContributionsByRepository(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
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
                                                            labels(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    name 
                                                                    color
                                                                    description
                                                                    createdAt
                                                                    isDefault
                                                                }}
                                                            }}
                                                            languages(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    color
                                                                    id
                                                                    name
                                                                }}
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
                                                }}
                                                repositoryContributions(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        isRestricted
                                                        occurredAt
                                                        resourcePath
                                                        url
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
                                                            labels(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    name 
                                                                    color
                                                                    description
                                                                    createdAt
                                                                    isDefault
                                                                }}
                                                            }}
                                                            languages(handle_pagination) {{
                                                                totalCount
                                                                nodes {{
                                                                    color
                                                                    id
                                                                    name
                                                                }}
                                                            }}
                                                            primaryLanguage {{
                                                                id
                                                                color
                                                                name
                                                            }}
                                                        }}
                                                    }}
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
                                            enterprises {{
                                                totalCount
                                            }}
                                            followers {{
                                                totalCount
                                            }}
                                            following {{
                                                totalCount
                                            }}
                                            gistComments(handle_pagination) {{
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
                                            isSponsoredBy
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
                                            topRepositories(handle_pagination) {{
                                                totalCount
                                            }}
                                            totalSponsorshipAmountAsSponsorInCents
                                            twitterUsername
                                            updatedAt  
                                            __typename
                                            }} 
                                        }} 
                                    }}
                                    blame {{
                                        ranges {{
                                            startingLine
                                            endingLine 
                                            age
                                        }}
                                    }}
                                    commitResourcePath
                                    commitUrl
                                    committedDate
                                    committer {{
                                        id
                                        databaseId
                                        avatarUrl
                                        email
                                        name
                                        login
                                        createdAt
                                        __typename 
                                    }}
                                    deletions
                                    file {{
                                        oid
                                        language
                                        extension
                                        lineCount
                                        name 
                                        path
                                        size 
                                        type
                                        history(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                abbreviatedOid
                                                id
                                                oid
                                                message
                                                messageBody
                                                messageHeadline
                                                url
                                            }}
                                        }}
                                        resourcePath
                                        treeUrl    
                                    }} 
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
                        fulldatabaseId
                        comments(handle_pagination) {{
                            totalCount
                            nodes {{
                                id
                                databaseId
                                author {{
                                    id
                                    databaseId
                                    __typename
                                    login
                                    url
                                    avatarUrl
                                    name
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
                                                    contributions(handle_pagination) {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                                months
                                                totalContributions
                                                weeks
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resorucePath
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions(handle_pagination) {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                            pullRequestReviewContributionsByRepository(handle_pagination) {{
                                                totalCount
                                                nodes {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                            }}
                                            repositoryContributions(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                }}
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
                                        enterprises {{
                                            totalCount
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(handle_pagination) {{
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
                                        isSponsoredBy
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
                                        topRepositories(handle_pagination) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt  
                                        __typename
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
                                    }}
                                }}
                                minimizedReason
                                publishedAt
                                reactions(handle_pagination) {{
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
                        fulldatabaseId
                        closingIssuesReferences(handle_pagination) {{
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
                                assignedActors(handle_pagination) {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    name
                                    __typename 
                                }}
                                author {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    name
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
                                                    contributions(handle_pagination) {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                                months
                                                totalContributions
                                                weeks
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resorucePath
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions(handle_pagination) {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                            pullRequestReviewContributionsByRepository(handle_pagination) {{
                                                totalCount
                                                nodes {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                            }}
                                            repositoryContributions(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                }}
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
                                        enterprises {{
                                            totalCount
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(handle_pagination) {{
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
                                        isSponsoredBy
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
                                        topRepositories(handle_pagination) {{
                                            totalCount
                                        }}
                                        totalSponsorshipAmountAsSponsorInCents
                                        twitterUsername
                                        updatedAt  
                                        __typename
                                    }} 
                                }}
                                authorAssociation
                                blockedBy(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        createdAt
                                        title
                                        url
                                        body
                                        bodyText
                                         labels(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                name 
                                                color
                                                description
                                                createdAt
                                                isDefault
                                            }}
                                        }}
                                        closed
                                        closedAt
                                    }}
                                }}
                                blocking(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        id
                                        databaseId
                                        createdAt
                                        title
                                        url
                                        body
                                        bodyText
                                         labels(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                name 
                                                color
                                                description
                                                createdAt
                                                isDefault
                                            }}
                                        }}
                                        closed
                                        closedAt
                                    }}
                                }}
                                labels(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        name 
                                        color
                                        description
                                        createdAt
                                        isDefault
                                    }}
                                }}
                                closed
                                closedAt
                                closedByPullRequestsReferences(handle_pagination) {{
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
                                        canbeRebased
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
                                comments(handle_pagination) {{
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
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    email
                                    name
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
                                issueFieldValues(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        id
                                        value
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
                                linkedBranches(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
                                    }}
                                    createdAt
                                    closed
                                    closedAt 
                                }}
                                participants(handle_pagination) {{
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
                                reactions(handle_pagination) {{
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
                                subIssues(handle_pagination) {{
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
                                        labels(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                name 
                                                color
                                                description
                                                createdAt
                                                isDefault
                                            }}
                                        }}
                                    }}
                                }}
                                subIssuesSummary {{
                                    completed
                                    percentCompleted
                                    total
                                }}
                                timelineItems(handle_pagination) {{
                                    totalCount
                                    filteredCount
                                    updatedAt
                                    nodes {{
                                        id
                                        createdAt
                                        __typename
                                    }}
                                }}
                                trackedInIssues(handle_pagination) {{
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
                                        labels(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                name 
                                                color
                                                description
                                                createdAt
                                                isDefault
                                            }}
                                        }}
                                    }}
                                }}
                                trackedIssues(handle_pagination) {{
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
                                        labels(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                name 
                                                color
                                                description
                                                createdAt
                                                isDefault
                                            }}
                                        }}
                                    }}
                                }}
                                trackedIssuesCount
                                updatedAt
                                userContentEdits(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        id
                                        createdAt
                                        deletedAt
                                        deletedBy
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
                        fulldatabaseId
                        baseRepository {{
                            id
                            databaseId
                            allowUpdateBranch
                            createdAt
                            archivedAt
                            autoMergeAllowed
                            visibility
                            forkCount
                            collaborators(handle_pagination) {{
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
                                            contributions(handle_pagination) {{
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
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
                                        months
                                        totalContributions
                                        weeks
                                    }}
                                    contributionYears
                                    doesEndInCurrentMonth
                                    endedAt
                                    firstIssueContribution {{
                                        ... on CreatedIssueContribution {{
                                            isRestricted
                                            occurredAt
                                            resorucePath
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
                                            labels(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    name 
                                                    color
                                                    description
                                                    createdAt
                                                    isDefault
                                                }}
                                            }}
                                            languages(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    color
                                                    id
                                                    name
                                                }}
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions(handle_pagination) {{
                                            totalCount
                                        }}
                                    }}
                                    pullRequestContributions(handle_pagination) {{
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
                                            labels(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    name 
                                                    color
                                                    description
                                                    createdAt
                                                    isDefault
                                                }}
                                            }}
                                            languages(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    color
                                                    id
                                                    name
                                                }}
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
                                    pullRequestReviewContributionsByRepository(handle_pagination) {{
                                        totalCount
                                        nodes {{
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
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
                                    }}
                                    repositoryContributions(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                        }}
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
                                    enterprises {{
                                        totalCount
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(handle_pagination) {{
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
                                    isSponsoredBy
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
                                    topRepositories(handle_pagination) {{
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
                            discussionCategories {{
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
                            discussions(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
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
                            forks(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
                                    }}
                                    languages(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            color
                                            id
                                            name
                                        }}
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
                            issueTypes(handle_pagination) {{
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
                            labels(handle_pagination) {{
                                totalCount
                                nodes {{
                                    name 
                                    color
                                    description
                                    createdAt
                                    isDefault
                                }}
                            }}
                            languages(handle_pagination) {{
                                totalCount
                                nodes {{
                                    color
                                    id
                                    name
                                }}
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
                                labels(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        name 
                                        color
                                        description
                                        createdAt
                                        isDefault
                                    }}
                                }}
                                languages(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        color
                                        id
                                        name
                                    }}
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
                            refs {{
                                totalCount
                            }}
                            releases(handle_pagination) {{
                                totalCount
                            }}
                            repositoryTopics(handle_pagination) {{
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
                            stargazers(handle_pagination) {{
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
                            submodules(handle_pagination) {{
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
                                labels(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        name 
                                        color
                                        description
                                        createdAt
                                        isDefault
                                    }}
                                }}
                                languages(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        color
                                        id
                                        name
                                    }}
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}       
                            }}
                            url
                            watchers
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
                            collaborators(handle_pagination) {{
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
                                            contributions(handle_pagination) {{
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
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
                                        months
                                        totalContributions
                                        weeks
                                    }}
                                    contributionYears
                                    doesEndInCurrentMonth
                                    endedAt
                                    firstIssueContribution {{
                                        ... on CreatedIssueContribution {{
                                            isRestricted
                                            occurredAt
                                            resorucePath
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
                                            labels(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    name 
                                                    color
                                                    description
                                                    createdAt
                                                    isDefault
                                                }}
                                            }}
                                            languages(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    color
                                                    id
                                                    name
                                                }}
                                            }}
                                            primaryLanguage {{
                                                id
                                                color
                                                name
                                            }}
                                        }}
                                        contributions(handle_pagination) {{
                                            totalCount
                                        }}
                                    }}
                                    pullRequestContributions(handle_pagination) {{
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
                                            labels(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    name 
                                                    color
                                                    description
                                                    createdAt
                                                    isDefault
                                                }}
                                            }}
                                            languages(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    color
                                                    id
                                                    name
                                                }}
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
                                    pullRequestReviewContributionsByRepository(handle_pagination) {{
                                        totalCount
                                        nodes {{
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
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
                                    }}
                                    repositoryContributions(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            isRestricted
                                            occurredAt
                                            resourcePath
                                            url
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                        }}
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
                                    enterprises {{
                                        totalCount
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(handle_pagination) {{
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
                                    isSponsoredBy
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
                                    topRepositories(handle_pagination) {{
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
                            discussionCategories {{
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
                            discussions(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
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
                            forks(handle_pagination) {{
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
                                    labels(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            name 
                                            color
                                            description
                                            createdAt
                                            isDefault
                                        }}
                                    }}
                                    languages(handle_pagination) {{
                                        totalCount
                                        nodes {{
                                            color
                                            id
                                            name
                                        }}
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
                            issueTypes(handle_pagination) {{
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
                            labels(handle_pagination) {{
                                totalCount
                                nodes {{
                                    name 
                                    color
                                    description
                                    createdAt
                                    isDefault
                                }}
                            }}
                            languages(handle_pagination) {{
                                totalCount
                                nodes {{
                                    color
                                    id
                                    name
                                }}
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
                                labels(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        name 
                                        color
                                        description
                                        createdAt
                                        isDefault
                                    }}
                                }}
                                languages(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        color
                                        id
                                        name
                                    }}
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
                            refs {{
                                totalCount
                            }}
                            releases(handle_pagination) {{
                                totalCount
                            }}
                            repositoryTopics(handle_pagination) {{
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
                            stargazers(handle_pagination) {{
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
                            submodules(handle_pagination) {{
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
                                labels(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        name 
                                        color
                                        description
                                        createdAt
                                        isDefault
                                    }}
                                }}
                                languages(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        color
                                        id
                                        name
                                    }}
                                }}
                                primaryLanguage {{
                                    id
                                    color
                                    name
                                }}       
                            }}
                            url
                            watchers
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
                        fulldatabaseId
                        editor {{
                            id
                            databaseId
                            login
                            name
                            url
                            avatarUrl
                            __typename
                        }}
                        assignedActors(handle_pagination) {{
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
                                    teams(handle_pagination) {{
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
                                    domains(handle_pagination) {{
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
                                            owner {{
                                                id
                                                databaseId
                                                login
                                                __typename
                                            }}
                                            verificationToken 
                                        }}
                                    }}
                                    hasSponsorsListing
                                    isSponsoredBy
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
                                    memberStatuses(handle_pagination) {{ 
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
                                    membersWithRole(handle_pagination) {{
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
                                          enterprises {{
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
                                        isSponsoredBy
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
                                        repositoryDiscussion {{
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
                                        topRepositories {{
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
                                          enterprises {{
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
                                        isSponsoredBy
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
                                        repositoryDiscussion {{
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
                                        topRepositories {{
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
                                    teams(handle_pagination) {{
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
                                    domains(handle_pagination) {{
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
                                            owner {{
                                                id
                                                databaseId
                                                login
                                                __typename
                                            }}
                                            verificationToken 
                                        }}
                                    }}
                                    hasSponsorsListing
                                    isSponsoredBy
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
                                    memberStatuses(handle_pagination) {{ 
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
                                    membersWithRole(handle_pagination) {{
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
                                          enterprises {{
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
                                        isSponsoredBy
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
                                        repositoryDiscussion {{
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
                                        topRepositories {{
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
                                                contributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                                months
                                                totalContributions
                                                weeks
                                            }}
                                            contributionYears
                                            doesEndInCurrentMonth
                                            endedAt
                                            firstIssueContribution {{
                                                ... on CreatedIssueContribution {{
                                                    isRestricted
                                                    occurredAt
                                                    resorucePath
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                                contributions(handle_pagination) {{
                                                    totalCount
                                                }}
                                            }}
                                            pullRequestContributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                            pullRequestReviewContributionsByRepository(handle_pagination) {{
                                                totalCount
                                                nodes {{
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
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
                                            }}
                                            repositoryContributions(handle_pagination) {{
                                                totalCount
                                                nodes {{
                                                    isRestricted
                                                    occurredAt
                                                    resourcePath
                                                    url
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
                                                        labels(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                name 
                                                                color
                                                                description
                                                                createdAt
                                                                isDefault
                                                            }}
                                                        }}
                                                        languages(handle_pagination) {{
                                                            totalCount
                                                            nodes {{
                                                                color
                                                                id
                                                                name
                                                            }}
                                                        }}
                                                        primaryLanguage {{
                                                            id
                                                            color
                                                            name
                                                        }}
                                                    }}
                                                }}
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
                                        enterprises {{
                                            totalCount
                                        }}
                                        followers {{
                                            totalCount
                                        }}
                                        following {{
                                            totalCount
                                        }}
                                        gistComments(handle_pagination) {{
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
                                        isSponsoredBy
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
                                        topRepositories(handle_pagination) {{
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
                                                contributions(handle_pagination) {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                            months
                                            totalContributions
                                            weeks
                                        }}
                                        contributionYears
                                        doesEndInCurrentMonth
                                        endedAt
                                        firstIssueContribution {{
                                            ... on CreatedIssueContribution {{
                                                isRestricted
                                                occurredAt
                                                resorucePath
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
                                                }}
                                                primaryLanguage {{
                                                    id
                                                    color
                                                    name
                                                }}
                                            }}
                                            contributions(handle_pagination) {{
                                                totalCount
                                            }}
                                        }}
                                        pullRequestContributions(handle_pagination) {{
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
                                                labels(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        name 
                                                        color
                                                        description
                                                        createdAt
                                                        isDefault
                                                    }}
                                                }}
                                                languages(handle_pagination) {{
                                                    totalCount
                                                    nodes {{
                                                        color
                                                        id
                                                        name
                                                    }}
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
                                        pullRequestReviewContributionsByRepository(handle_pagination) {{
                                            totalCount
                                            nodes {{
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
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
                                        }}
                                        repositoryContributions(handle_pagination) {{
                                            totalCount
                                            nodes {{
                                                isRestricted
                                                occurredAt
                                                resourcePath
                                                url
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
                                                    labels(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            name 
                                                            color
                                                            description
                                                            createdAt
                                                            isDefault
                                                        }}
                                                    }}
                                                    languages(handle_pagination) {{
                                                        totalCount
                                                        nodes {{
                                                            color
                                                            id
                                                            name
                                                        }}
                                                    }}
                                                    primaryLanguage {{
                                                        id
                                                        color
                                                        name
                                                    }}
                                                }}
                                            }}
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
                                    enterprises {{
                                        totalCount
                                    }}
                                    followers {{
                                        totalCount
                                    }}
                                    following {{
                                        totalCount
                                    }}
                                    gistComments(handle_pagination) {{
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
                                    isSponsoredBy
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
                                    topRepositories(handle_pagination) {{
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
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                mergedBy {{
                                    id
                                    databaseId
                                    createdAt
                                    avatarUrl
                                    login
                                    resourcePath
                                    url
                                    __typename 
                                }}
                                participants(handle_pagination) {{
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
                                suggestedActors(handle_pagination) {{
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
                                suggestedReviewerActors(handle_pagination) {{
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
                                suggestedReviewers(handle_pagination) {{
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
                                userContentEditConnection(handle_pagination) {{
                                    totalCount
                                    nodes {{
                                        id
                                        createdAt
                                        deletedAt
                                        editedAt
                                        updatedAt
                                        diff
                                    }}
                                }}
                            }}
                        }}
                    }}          
                """
        return query
             
                            
     