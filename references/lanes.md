# Scaling the series: one example, then lanes

## Gate: one approved example

Do not start the series until the user has seen one finished page live (or rendered) and
said yes. Their remarks on the first page are worth more than any rule here.

## Unit of work

One item per session, all languages of that item in the same session. A session ends
with: research notes saved, `guides/<slug>.json` written, checker green for that file and
for the whole set (the shared-sentence rule spans pages), one commit.

## Parallel lanes

Up to three lanes run at the same time. More rarely pays: the bottleneck becomes the
usage limit, and on a small server the RAM.

- **Each lane is a separate clone** of the repository, not a worktree of the same one.
  Tools that judge a session by comparing every git ref before and after (a nightly
  relauncher, a CI guard) see the other lane's branch move and stop. Separate clones also
  let you merge into the main branch while lanes run.
- **Disjoint item lists**: split the item list into lanes before starting, written in each
  lane's plan. Two lanes never take the same item.
- **The plan file belongs to the lane branch.** If the plan is committed on the main
  branch and the lane changes it, merging brings it back to main, and the next lane's plan
  is overwritten. Keep `plan.md` per lane, or outside the repository.
- **Expected merge conflicts**: an index file listing the guides, and a progress file.
  Resolve by union; never drop a lane's entry.

### With the autonomous-relaunch skill

If the `autonomous-relaunch` skill is installed, each lane is one project:

```bash
R=~/.claude/skills/autonomous-relaunch/scripts/relaunch.py
git clone <repo> ~/autonomous-relaunch/clones/<site>-a   # and -b, -c
$R setup ~/autonomous-relaunch/clones/<site>-a --check "python3 ~/.claude/skills/sourced-guide/scripts/check_guide.py guides/*.json --floor guides/floor.json" --sessions 3
```

The plan template in `assets/plan.lane.md` lists the items of one lane, one task each,
with a *done when* the checker decides.

### Without it

Run sessions by hand or with subagents, one per item, each told: the item, SERIES.md,
the floor, the notes path, and "write the JSON and run the checker before you stop".
Collect, run the checker on the whole set, fix, then publish.

## Publishing

- Publish between runs, never while a lane session is running on the same branch.
- Publish through the site's normal path (its API, its deploy script), never by writing
  to the production database by hand.
- After publishing, open two or three pages as a visitor would and check the rendered
  text: markers turned into links, no raw Markdown, structured data as SERIES.md says,
  the listing page counts the new pages (caches can hide them for an hour or more).
