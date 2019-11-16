# -*- coding: utf-8 -*-
import os
import sys
from typing import Callable
from typing import FrozenSet
from typing import Optional
from typing import Tuple
from xml.dom import minidom

import cairosvg
import pandas as pd

if getattr(sys, 'frozen', False):
    # Running as all-in-one executable.
    bundle_dir = sys._MEIPASS
    cur_dir = os.path.dirname(sys.executable)
else:
    # Running as a console script.
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    cur_dir = os.getcwd()


SVG_FORMAT = 'SVG'
PNG_FORMAT = 'PNG'

DEFAULT_COLOR = '#aec0d2'

COLUMN_IDS = frozenset([
    'Eco_Inlet',
    'Eco_Outlet',
    'IP_Turbine_Outlet',
    'Tapping_A6',
    'Tapping_A4',
    'Tapping_A3',
    'Tapping_A2',
    'Feedwatertank',
    'Condensate_LPP_A3_Inlet',
    'Condensate_LPP_A2_Inlet',
    'Condensate_LPP_A3_Outlet',
    'Condensate_LPP_A2_Outlet',
    'Condensate_LPP_A4_Outlet',
    'Condenser_Outlet',
    'Condensatepump_Outlet',
    'HPP_A6_Outlet',
    'Tapping_A5',
    'Tapping_A1',
    'Condenser_Inlet',
    'HPP_A7_Outlet',
    'SH1_Outlet',
    'Evaporator_Outlet',
    'SH3_Outlet',
    'Feedwaterpumps_Outlet',
    'Livesteam',
    'Hot_Reheat',
    'Cold_Reheat',
])


def load_measurements(input_file: str,
                      debug: bool = False) -> Tuple[pd.DataFrame,
                                                    pd.DataFrame]:
    df = pd.read_excel(
        os.path.expanduser(input_file),
        skiprows=[0, 1, 2],
        header=[0],
        # usecols='A,AD,AH:AP,AT:BQ',
        index_col=0)

    df.set_index(pd.to_timedelta(df.index, unit='s'),
                 drop=True, inplace=True)
    df.rename_axis('Time', axis=0, inplace=True)

    if debug:
        rc, cc = df.shape
        print(f'Loaded {input_file!r} ({rc} rows, {cc} columns)')

    columns = df.columns
    temperature = columns[columns.str.startswith('Temperature')]
    pressure = columns[columns.str.startswith('Pressure')]

    if debug:
        print('Pressure columns:\n\t{}\n'.format(
            '\n\t'.join(sorted(pressure.tolist()))))

        print('Temperature columns:\n\t{}\n'.format(
            '\n\t'.join(sorted(temperature.tolist()))))

    pressures = df.loc(axis=1)[pressure].copy()
    pressures.columns = pressure.str.replace(
        r'^Pressure\s', '').str.replace(r'[\s-]', '_')
    pressures.rename_axis('Pressure', axis=1, inplace=True)

    temperatures = df.loc(axis=1)[temperature].copy()
    temperatures.columns = temperature.str.replace(
        r'^Temperature\s', '').str.replace(r'[\s-]', '_')
    temperatures.columns.name = 'Temperature'
    temperatures.rename_axis('Pressure', axis=1, inplace=True)

    return pressures, temperatures


def load_cleaned(input_file: str,
                 debug: bool = False) -> Tuple[pd.DataFrame,
                                               pd.DataFrame]:

    temperatures = pd.read_excel(
        os.path.expanduser(input_file),
        sheet_name='Temperatures',
        header=0)
    temperatures.index = pd.to_timedelta(temperatures.Time, unit='s')
    temperatures.drop('Time', axis=1, inplace=True)

    if debug:
        rc, cc = temperatures.shape
        print(f'Loaded temperatures {input_file!r} ({rc} rows, {cc} columns)')

    pressures = pd.read_excel(
        os.path.expanduser(input_file),
        sheet_name='Pressures',
        header=0)
    pressures.index = pd.to_timedelta(pressures.Time, unit='s')
    pressures.drop('Time', axis=1, inplace=True)

    if debug:
        rc, cc = pressures.shape
        print(f'Loaded pressures {input_file!r} ({rc} rows, {cc} columns)')

    return pressures, temperatures


def save_cleaned(pressures: pd.DataFrame,
                 temperatures: pd.DataFrame,
                 output_file: str,
                 output_dir: str) -> None:

    if os.path.dirname(output_file) == '':
        output_file = os.path.join(output_dir, output_file)
    else:
        output_file = os.path.expanduser(output_file),

    writer = pd.ExcelWriter(
        output_file,
        engine='xlsxwriter')

    pressures = pressures.copy()
    pressures_seconds = pressures.index.seconds
    pressures.reset_index(inplace=True)
    pressures['Time'] = pressures_seconds
    pressures.to_excel(
        writer, 'Pressures',
        index=False,
        freeze_panes=(1, 1))

    temperatures = temperatures.copy()
    temperatures_seconds = temperatures.index.seconds
    temperatures.reset_index(inplace=True)
    temperatures['Time'] = temperatures_seconds
    temperatures.to_excel(
        writer, 'Temperatures',
        index=False,
        freeze_panes=(1, 1))

    sheet = writer.sheets['Pressures']
    sheet.set_zoom(80)
    sheet.set_column(1, len(pressures.columns), 25)

    sheet = writer.sheets['Temperatures']
    sheet.set_zoom(80)
    sheet.set_column(1, len(temperatures.columns), 25)

    writer.save()


def load_xml_groups(
        input_file: str,
        ids: FrozenSet[str]) -> Tuple[minidom.Document,
                                      pd.DataFrame]:

    filename = os.path.expanduser(input_file)
    doc = minidom.parse(filename)

    groups = pd.DataFrame.from_records(
        {'id': group.attributes['id'].value,
         'temp': DEFAULT_COLOR,
         'pressure': 1.0,
         'paths': len(group.childNodes)}
        for group in doc.getElementsByTagName('g')
        if group.attributes['id'].value in ids)
    groups = groups.set_index('id').sort_index()

    return doc, groups


def update_xml_groups(
        doc: minidom.Document,
        groups: pd.DataFrame) -> minidom.Document:

    doc = doc.cloneNode(True)
    for row in groups.itertuples():
        for group in doc.getElementsByTagName('g'):
            group_id = group.attributes['id'].value
            if group_id != row.Index:
                continue
            temp_color = row.temp
            pressure_width = row.pressure

            for path in group.childNodes:
                if path.nodeType != minidom.Element.ELEMENT_NODE:
                    continue

                del path.attributes['style']
                path.setAttribute('stroke', temp_color)
                path.setAttribute('fill', temp_color)
                path.setAttribute('stroke-width', str(pressure_width))

    return doc


def save_xml(
        doc: minidom.Document,
        output_file: str) -> None:

    filename = os.path.expanduser(output_file)
    with open(filename, 'wt', encoding='utf-8') as f:
        f.write(doc.toprettyxml())
        f.flush()


def save_output(
        doc: minidom.Document,
        output_file: str,
        output_format: str) -> None:

    if output_format == PNG_FORMAT:

        rect = doc.createElement('rect')
        rect.setAttribute('width', '100%')
        rect.setAttribute('height', '100%')
        rect.setAttribute('fill', 'white')
        doc.documentElement.insertBefore(
            rect, doc.documentElement.childNodes[0])

    save_xml(doc, output_file)

    if output_format == PNG_FORMAT:
        output_base, _ = os.path.splitext(output_file)
        output_png = output_base + '.png'

        with open(output_file, 'rb') as fp:
            cairosvg.svg2png(
                file_obj=fp,
                write_to=output_png,
                dpi=96,
                scale=2,
                parent_width=800,
                parent_height=600)

        os.remove(output_file)
        output_file = output_png

    print(f'Saved {output_format} {output_file!r}')


def pressure_to_width(pressure):

    LOW_HIGH_TO_WIDTH = {
        (-2,   2): 1,
        (3,  13): 1.5,
        (14,  30): 2,
        (31,  60): 2.5,
        (61, 150): 3,
        (151, 320): 4,
    }

    for (low, high), width in LOW_HIGH_TO_WIDTH.items():
        if low <= pressure <= high:
            return width


def temperature_to_color(temperature):

    REDS = [(0.47607843137254902, 0.19424836601307194, 0.18117647058823527),
            (0.75215686274509819, 0.1884967320261437, 0.16235294117647048),
            (0.90980392156862755, 0.27372549019607845, 0.22405228758169926),
            (0.9490196078431371, 0.44993464052287591, 0.36627450980392162)]

    BLUES = [(0.77524029219530965, 0.85830065359477103, 0.9368242983467896),
             (0.41708573625528633, 0.68063052672049218, 0.83823144944252215),
             (0.12710495963091117, 0.4401845444059978, 0.70749711649365632)]

    LOW_HIGH_TO_COLOR = {

        (0, 35): BLUES[0],     # light blue
        (36, 80): BLUES[1],    # blue
        (81, 160): BLUES[2],   # dark blue
        (161, 250): REDS[3],   # light red
        (251, 300): REDS[2],   # red
        (301, 400): REDS[1],   # darker red
        (401, 9999): REDS[0],  # darkest red
    }

    for (low, high), color in LOW_HIGH_TO_COLOR.items():
        if low <= temperature <= high:
            return color


def main(
        raw_table: str='Measurement.xlsx',
        cleaned_table: str='Pressures_Temperatures.xlsx',
        input_svg: str='PowerPlant.svg',
        output_dir: str=cur_dir + os.path.sep,
        output_format: str=SVG_FORMAT,
        debug: bool = False,
        custom_raw_table: bool = False,
        percent_done: Optional[Callable[[float], bool]] = None

) -> None:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib import colors as mcolors

    os.makedirs(output_dir, exist_ok=True)

    if custom_raw_table:
        pres, temps = load_measurements(raw_table, debug)
        save_cleaned(pres, temps, cleaned_table, output_dir)

    else:
        try:
            # Try loading the cleaned version of the table if it exists.
            pres, temps = load_cleaned(cleaned_table, debug)

        except IOError:
            # Load the original table and save a cleaned version.
            pres, temps = load_measurements(raw_table, debug)
            save_cleaned(pres, temps, cleaned_table, output_dir)

    input_svg_abspath = os.path.realpath(
        os.path.join(cur_dir, input_svg))
    print(f'Loading SVG from {input_svg_abspath}...')

    doc, groups = load_xml_groups(input_svg_abspath, COLUMN_IDS)

    last_row_seconds = temps.last_valid_index().seconds
    print(f'Saving {len(temps)} output files...')
    for row1, row2 in zip(temps.itertuples(), pres.itertuples()):
        time_prefix = str(row1.Index.seconds)
        groups['temp'] = DEFAULT_COLOR

        for col in temps.columns:
            val = temps.loc[row1.Index, col]
            color = temperature_to_color(val)
            hexcolor = mcolors.rgb2hex(mcolors.to_rgba(color))
            groups.loc[col, 'temp'] = hexcolor

        for col in pres.columns:
            val = pres.loc[row2.Index, col]
            width = pressure_to_width(val)
            groups.loc[col, 'pressure'] = width

        updated_doc = update_xml_groups(doc, groups)
        output_file = f'{output_dir}{time_prefix}-{input_svg}'
        save_output(updated_doc, output_file, output_format)

        if percent_done:
            percent = row1.Index.seconds / last_row_seconds
            should_continue = percent_done(percent)
            if not should_continue:
                break


if __name__ == '__main__':
    main()
