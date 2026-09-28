"""Build a shared frame-aligned edit timeline from reviewed source-time cuts."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path


def balanced_sum(items):
    if not items:
        return '0'
    if len(items) == 1:
        return items[0]
    mid = len(items) // 2
    return '(' + balanced_sum(items[:mid]) + '+' + balanced_sum(items[mid:]) + ')'


def map_time(source_time, keep, speed):
    return sum(max(0.0, min(source_time, b) - a) for a, b in keep) / speed


def build_timeline(plan):
    duration = float(plan['duration'])
    rate = Fraction(str(plan['fps']))
    fps = float(rate)
    speed = float(plan.get('speed', 1.12))
    if not all(math.isfinite(v) for v in (duration, fps, speed)):
        raise ValueError('duration, fps and speed must be finite')
    if duration <= 0 or fps <= 0 or not 0.5 <= speed <= 2:
        raise ValueError('Positive duration/fps and speed in [0.5, 2] required')
    frame_count = int(plan.get('source_frames', round(duration * fps)))
    if frame_count < 1:
        raise ValueError('Source has no frames')
    cuts = []
    for item in plan.get('cuts', []):
        a, b = (item['start'], item['end']) if isinstance(item, dict) else item
        a, b = float(a), float(b)
        if not math.isfinite(a) or not math.isfinite(b) or b < a:
            raise ValueError('Every cut requires finite start <= end')
        a, b = max(0, min(frame_count, round(a * fps))), max(0, min(frame_count, round(b * fps)))
        if b > a:
            cuts.append([a, b])
    merged = []
    for a, b in sorted(cuts):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    keep_frames, cursor = [], 0
    for a, b in merged:
        if a > cursor:
            keep_frames.append([cursor, a])
        cursor = b
    if cursor < frame_count:
        keep_frames.append([cursor, frame_count])
    if not keep_frames:
        raise ValueError('The plan removes the entire source')
    keep = [[a / fps, b / fps] for a, b in keep_frames]
    mapping, output_cursor = [], 0.0
    for a, b in keep:
        end = output_cursor + (b - a) / speed
        mapping.append({'source_start': a, 'source_end': b,
                        'output_start': output_cursor, 'output_end': end})
        output_cursor = end
    return {
        'source_duration': duration, 'source_frames': frame_count,
        'fps': str(rate), 'speed': speed,
        'cuts': [[a / fps, b / fps] for a, b in merged],
        'keep': keep, 'keep_frames': keep_frames,
        'output_duration': output_cursor, 'mapping': mapping,
        'select_expr': balanced_sum([f'between(n,{a},{b-1})' for a, b in keep_frames]),
        'setpts_expr': f'N/(({rate.numerator}/{rate.denominator})*{speed}*TB)',
        'atempo_filter': f'atempo={speed}',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build_timeline(json.loads(args.plan.read_text(encoding='utf-8-sig')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"{len(result['keep'])} retained intervals; {result['output_duration']:.3f} seconds")


if __name__ == '__main__':
    main()
