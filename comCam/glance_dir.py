import os
import glob
import shutil
import lsst.sims.maf.batches as batches
import lsst.sims.maf.db as db
import lsst.sims.maf.metricBundles as mb


if __name__ == "__main__":
    """
    Run the glance batch on all .db files in a directory.
    """
    db_files = glob.glob('*.db')
    run_names = [name.replace('.db', '') for name in db_files]
    if os.path.isfile('trackingDb_sqlite.db'):
        os.remove('trackingDb_sqlite.db')
    for name in run_names:
        if os.path.isdir(name):
            shutil.rmtree(name)
        opsdb = db.OpsimDatabaseV4(name+'.db')
        colmap = batches.ColMapDict('OpsimV4')

        bdict = {}
        bdict.update(batches.glanceBatch(colmap, name, slicer_camera='ComCam'))
        bdict.update(batches.fOBatch(colmap, name))
        resultsDb = db.ResultsDb(outDir=name)
        group = mb.MetricBundleGroup(bdict, opsdb, outDir=name, resultsDb=resultsDb)
        group.runAll()
        group.plotAll()
        resultsDb.close()
        opsdb.close()
        db.addRunToDatabase(name, 'trackingDb_sqlite.db', None, name, '', '', name+'.db')
