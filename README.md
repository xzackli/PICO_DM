# PICO_DM

It looks like orphics, Mat's library for lensing-related stuff, is slightly broken on the current master commit. To install, first clone https://github.com/msyriac/orphics and then run

```
git checkout -b historical_branch 5a980eb48b95f58a41ce9a280d369973d0d2155e
```

This will move you to the branch that I used when making the forecasts. Next, go into the orphics directory and install both the prerequisites and orphics itself.

```
pip install seaborn healpy camb --user
python setup.py install
```

Now you should be able to run the SO experiments example notebook in this repo.
