# Traps already paid for

Each of these cost a night or a page before the rule existed.

1. **Two worktrees of one repository stop each other.** A relauncher that checks that no
   other ref moved sees the other lane's branch advance and ends the night. Use separate
   clones, one per lane.

2. **Sessions cut during research.** A session can end on a usage limit or a timeout in
   the middle of reading sources. Research held only in context is lost and paid twice.
   Write each fact to `guides/research/<slug>.md` as soon as it is read; a new session
   starts by reading that file.

3. **The plan overflowing onto the main branch.** A plan committed on main, edited by a
   lane, came back to main at merge and replaced the next lane's plan. Keep each lane's
   plan on its own branch or outside the repository.

4. **A flaky check is worse than none.** A floor test that fetched URLs failed on a slow
   network and stopped a night for nothing. The checker reads files only: link checking
   is a separate, manual step, never part of the session's pass or fail.

5. **Usage limits.** Three lanes in parallel exhaust a subscription faster than one lane
   three times as long, and the cut lands mid-page. Size each session to one item, start
   with fewer lanes, and expect the last session of a night to be cut.

6. **The template that looked fine before it was filled.** A title or meta description
   built from a template is measured after filling, with the longest real value. A
   country name or an organisation name from a database can push it past the limit.

7. **Structured data that the page cannot back.** `JobPosting` on a page that invites
   people to sign up (and does not hire them) breaks the search engine's rules for that
   type and can cost the whole site its rich results. The same for `Review` without real
   reviews.

8. **Second-hand legal values.** A fee or a guarantee amount read on a consultant's blog
   was off by a factor of ten against the decree. Second-hand values are `null` until the
   official text is read.

9. **Listing pages that deny fresh data.** A pre-rendered listing kept saying "no page in
   this category" for an hour after publishing. After any publish, revalidate or purge
   the listing and the sitemap, and look at them.
