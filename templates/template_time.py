import warnings
import argparse
import glob
import os
import shutil

import rubin_sim.maf.metric_bundles as metric_bundles
import rubin_sim.maf.metrics as metrics
import rubin_sim.maf.slicers as slicers

from rubin_sim.maf.batches.common import standard_summary

import rubin_sim.maf.batches as batches
import rubin_sim.maf.db as db
import rubin_sim.maf.metric_bundles as mb


def tt_batch():

    standard_stats = standard_summary()
    bundle_list = []
    bands = 'ugrizy'
    for band in bands:
        sql = "band = '%s'" % band

        slicer = slicers.HealpixSlicer()
        metric = metrics.TemplateTime(seeing_percentile=100,
                                      m5_percentile=100,
                                      n_images_in_template=3,)

        bundle_list.append(metric_bundles.MetricBundle(metric, 
                                                       slicer, 
                                                       sql,
                                                       summary_metrics=standard_stats))

    bd = metric_bundles.make_bundles_dict_from_list(bundle_list)

    return bd


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=str, default=None)
    args = parser.parse_args()

    if args.db is None:
        db_files = glob.glob("*.db")
        db_files = [filename for filename in db_files if "trackingDb" not in filename]
    else:
        db_files = [args.db]
    run_names = [os.path.basename(name).replace(".db", "") for name in db_files]

    for filename, name in zip(db_files, run_names):
        if os.path.isdir(name + "_ttime"):
            shutil.rmtree(name + "_ttime")

        bdict = tt_batch()
        results_db = db.ResultsDb(out_dir=name + "_ttime")
        group = mb.MetricBundleGroup(
            bdict,
            filename,
            out_dir=name + "_ttime",
            results_db=results_db,
            save_early=False,
        )
        group.run_all(clear_memory=True, plot_now=True)
        results_db.close()
        db.add_run_to_database(
            maf_dir=name + "_ttime",
            tracking_db_file="trackingDb_sqlite.db",
            run_group=None,
            run_name=name,
            run_comment="",
            maf_comment="Template",
            db_file=name + ".db",
        )
