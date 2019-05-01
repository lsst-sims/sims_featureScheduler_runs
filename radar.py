import os
import glob
import shutil
import lsst.sims.maf.batches as batches
import lsst.sims.maf.db as db
import lsst.sims.maf.metricBundles as mb
import argparse


if __name__ == "__main__":
    """
    Run the radar batch on all .db files in a directory.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="OpSim database")
    args = parser.parse_args()
    filename = args.filename

    name = filename.replace('.db', '')

    outDir = 'radar_'+name

    if os.path.isdir(name):
        shutil.rmtree(name)

    opsdb = db.OpsimDatabaseV4(name+'.db')
    colmap = batches.ColMapDict('OpsimV4')

    bdict = {}
    bdict.update(batches.scienceRadarBatch(colmap, name))
    resultsDb = db.ResultsDb(outDir=name)
    group = mb.MetricBundleGroup(bdict, opsdb, outDir=outDir, resultsDb=resultsDb)
    group.runAll()
    group.plotAll()
    resultsDb.close()
    opsdb.close()
    db.addRunToDatabase(outDir, 'trackingDb_sqlite.db', None, name, '', '', name+'.db')
